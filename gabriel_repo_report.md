# Rapport de cartographie du dépôt Gabriel
**Racine analysée :** `C:\agent-multiloop-Gabriel-local-final`  
**Date :** 2026-08-17 11:33:28  
**Fichiers analysés :** 1179  
**Liens résolus :** 829  
**Références potentiellement cassées :** 1501

---

## 1. Arborescence complète
```
C:\agent-multiloop-Gabriel-local-final
├── .emergent
│   ├── cron
│   │   ├── applied.hash
│   │   ├── dispatch_webhook.sh
│   │   ├── watch_crons.sh
│   │   ├── webhook-crons
│   │   └── webhook_crond.sh
│   ├── emergent.yml
│   ├── summary.txt
│   └── system_deps.txt
├── .github
│   └── workflows
│       ├── build.yml
│       └── codacy.yml
├── agent-multiloop-Gabriel-local
│   ├── .github
│   │   └── workflows
│   │       ├── build.yml
│   │       └── tests.yml
│   ├── backend
│   │   └── multiloop_backend.py
│   ├── commande-gabriel
│   │   ├── AIDE-MEMOIRE.txt
│   │   ├── COMMANDES.md
│   │   └── README.md
│   ├── data
│   │   └── debats
│   ├── docs
│   │   ├── archive
│   │   │   ├── CLAUDE_API_KEY_LOCALISATION.md
│   │   │   ├── COGNITIVE_GAP_EXTENSION.md
│   │   │   ├── CORRECTION_TYPO_CLAUDE_KEY.md
│   │   │   ├── CORRECTIONS_7eME_LOOP.md
│   │   │   ├── FIX_NEGATIVE_NUMBERS.md
│   │   │   ├── GABRIEL_v6.0_CLAUDE_PRIORITAIRE.md
│   │   │   ├── GABRIEL_v6.0_EXECUTIVE_SUMMARY.md
│   │   │   ├── GABRIEL_v6.0_QUICK_REFERENCE.md
│   │   │   ├── GABRIEL_v6.1_GAP_MIXED_HOL4.md
│   │   │   ├── GABRIEL_v6.2_RAG_SEMANTIQUE.md
│   │   │   ├── GAP_DEPLOYMENT.md
│   │   │   ├── GAP_FORMULA_CORRECTION.md
│   │   │   ├── LLM_MANAGER_v2_MIGRATION.md
│   │   │   ├── META_LEARNING_EXPERTISE.md
│   │   │   ├── SECURITY_FIX.md
│   │   │   ├── SECURITY_GUIDE.md
│   │   │   ├── SETUP_FINAL.md
│   │   │   ├── SOLUTION_DEFINITIVE.md
│   │   │   ├── SYNTHESE_COMPLETE.md
│   │   │   └── test_result.md
│   │   ├── analysis_notes.md
│   │   ├── ARCHITECTURE_USER.md
│   │   ├── CORPUS_KNOWLEDGE.md
│   │   ├── geometrie_spectre_premiers.docx
│   │   ├── geometrie_spectre_premiers.tex
│   │   ├── PROMPT_CACHING_IMPLEMENTATION.md
│   │   └── psi_savard_comparison.tex
│   ├── examples
│   │   ├── example_prompt_caching.py
│   │   ├── verif_p103_n27_CORRECT.thy
│   │   └── verif_p59_n17_CORRECTED.thy
│   ├── guide_utilisateur
│   │   ├── 01_DEMARRAGE_RAPIDE
│   │   │   └── INDEX.md
│   │   ├── 02_MODE_CINEMATIQUE
│   │   │   └── INDEX.md
│   │   ├── 03_ANALYSE_IMAGES
│   │   │   └── INDEX.md
│   │   ├── 04_DEPLOIEMENT
│   │   │   └── INDEX.md
│   │   ├── 05_MATHEMATIQUES
│   │   │   └── INDEX.md
│   │   ├── 06_RECONSTRUCTION
│   │   │   └── INDEX.md
│   │   ├── 07_TESTS_VALIDATION
│   │   │   └── INDEX.md
│   │   ├── 08_CONFIGURATION
│   │   │   └── INDEX.md
│   │   ├── 09_COMMANDES_REFERENCES
│   │   │   └── INDEX.md
│   │   ├── 10_RAPPORTS_ANALYSES
│   │   │   └── INDEX.md
│   │   ├── 11_VERSIONS_RELEASES
│   │   │   └── INDEX.md
│   │   └── README.md
│   ├── logs
│   ├── memory
│   │   ├── __init__.py
│   │   ├── adaptateur_cognitif_rag.py
│   │   ├── banque_qr_methode_spectrale.md
│   │   ├── dictionnaire_spectral.py
│   │   ├── methode_spectral_section_XI.py
│   │   ├── methode_spectral_section_XII.py
│   │   ├── methode_spectral_section_XIII.py
│   │   └── prompt_injector_enhanced.py
│   ├── scripts
│   │   ├── healthcheck_tex.sh
│   │   ├── isabelle-integration.sh
│   │   ├── isabelle_static_check.py
│   │   ├── sync_theory_to_agent.py
│   │   ├── tex_healthcheck.py
│   │   └── translate_thy.py
│   ├── src
│   │   ├── adapters
│   │   │   ├── corpus
│   │   │   │   ├── __init__.py
│   │   │   │   ├── certainty_kernel.py
│   │   │   │   ├── thy_analyzer.py
│   │   │   │   └── thy_loader.py
│   │   │   ├── hol_isabelle
│   │   │   │   ├── __init__.py
│   │   │   │   └── isabelle_adapter.py
│   │   │   ├── llm
│   │   │   │   ├── __init__.py
│   │   │   │   ├── ollama_client.py
│   │   │   │   ├── openai_client.py
│   │   │   │   └── utf8_sanitizer.py
│   │   │   ├── wolfram
│   │   │   │   ├── __init__.py
│   │   │   │   └── wolfram_client.py
│   │   │   ├── __init__.py
│   │   │   ├── gabriel_isabelle_bridge.py
│   │   │   ├── gabriel_multiformat_manager.py
│   │   │   ├── gabriel_project_manager.py
│   │   │   └── hol_integration.py
│   │   ├── api
│   │   │   └── gabriel_http_api.py
│   │   ├── audit
│   │   │   ├── __init__.py
│   │   │   └── audit_store.py
│   │   ├── cognitive
│   │   │   ├── __init__.py
│   │   │   ├── engine_bridge.py
│   │   │   ├── epistemic.py
│   │   │   ├── meta_reasoning.py
│   │   │   ├── proof_trace.py
│   │   │   ├── regime_ontology.py
│   │   │   └── traced_calculations.py
│   │   ├── core
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── conversational_memory.py
│   │   │   ├── filesystem_access.py
│   │   │   ├── integrateur_memoire.py
│   │   │   ├── latex_generator.py
│   │   │   ├── llm_manager.py
│   │   │   ├── logging_setup.py
│   │   │   ├── orchestrator.py
│   │   │   ├── pipeline.py
│   │   │   ├── pipeline_with_gap_detection.py
│   │   │   ├── plan_trifocal.py
│   │   │   ├── plan_trifocal_avec_image.py
│   │   │   ├── planner.py
│   │   │   ├── scientific_badge.py
│   │   │   ├── spectral_core.py
│   │   │   └── types.py
│   │   ├── debug_toolkit
│   │   │   ├── __init__.py
│   │   │   ├── mpmath_validator.py
│   │   │   ├── registry.py
│   │   │   ├── sympy_validator.py
│   │   │   └── z3_prover.py
│   │   ├── engines
│   │   │   ├── abstraction
│   │   │   │   ├── __init__.py
│   │   │   │   └── abstraction_layer.py
│   │   │   ├── concept_navigation
│   │   │   │   ├── __init__.py
│   │   │   │   └── navigator.py
│   │   │   ├── generalization
│   │   │   │   ├── __init__.py
│   │   │   │   └── generalizer.py
│   │   │   ├── meta_reasoning
│   │   │   │   ├── __init__.py
│   │   │   │   └── meta_reasoning.py
│   │   │   ├── numerical_verification
│   │   │   │   ├── __init__.py
│   │   │   │   └── numerical_verifier.py
│   │   │   ├── theorem_discovery
│   │   │   │   ├── __init__.py
│   │   │   │   └── discovery_loop.py
│   │   │   ├── __init__.py
│   │   │   ├── geometrie_spectrale_engine.py
│   │   │   └── question_graphs.py
│   │   ├── learning
│   │   │   ├── debugging_expertise.py
│   │   │   ├── meta_learning_integration.py
│   │   │   └── slowmotion_recorder.py
│   │   ├── multiloop
│   │   │   ├── __init__.py
│   │   │   ├── certainty_model.py
│   │   │   ├── coherence_detector.py
│   │   │   ├── critic.py
│   │   │   ├── debat_orchestrator.py
│   │   │   ├── domain_classifier.py
│   │   │   ├── domain_gate.py
│   │   │   ├── forbidden_vocab.py
│   │   │   ├── gabriel_domain_config.py
│   │   │   ├── llm_reformulator.py
│   │   │   ├── logical_loop.py
│   │   │   ├── pre_reasoner.py
│   │   │   ├── refinement_loop.py
│   │   │   ├── refinement_loop_fixed.py
│   │   │   ├── request_decomposer.py
│   │   │   ├── request_decomposer_patch.py
│   │   │   ├── silent_audit.py
│   │   │   ├── slow_motion_debugger.py
│   │   │   ├── slowmotion_trigger.py
│   │   │   └── verification_loop.py
│   │   ├── spectral
│   │   │   ├── __init__.py
│   │   │   ├── _primes_data.py
│   │   │   ├── composite_absurdity_prover.py
│   │   │   ├── digamma.py
│   │   │   ├── digamma_pure.py
│   │   │   ├── gap_cognitive_model.py
│   │   │   ├── gap_compute.py
│   │   │   ├── gap_solver_corrected.py
│   │   │   ├── gap_validation.py
│   │   │   ├── gaps.py
│   │   │   ├── hol_script_generator.py
│   │   │   ├── plan_trifocal.py
│   │   │   ├── prime_table.py
│   │   │   ├── psi_savard.py
│   │   │   ├── ratios.py
│   │   │   ├── reconstructor.py
│   │   │   ├── rsp_command.py
│   │   │   ├── rsp_curve.py
│   │   │   ├── spectral_knowledge.py
│   │   │   ├── spectral_models.py
│   │   │   ├── suites.py
│   │   │   └── tchebychev_savard_pipeline.py
│   │   ├── ui
│   │   │   ├── __init__.py
│   │   │   ├── ask_gabriel.py
│   │   │   ├── ci_status.py
│   │   │   ├── cinematic_display.py
│   │   │   ├── cinematic_orchestrator.py
│   │   │   ├── cli.py
│   │   │   ├── complexity_analyzer.py
│   │   │   ├── debug_session.py
│   │   │   ├── keybindings.py
│   │   │   └── latex_commands.py
│   │   ├── visualization
│   │   │   ├── __init__.py
│   │   │   ├── ascii_renderer.py
│   │   │   ├── auto_trigger.py
│   │   │   ├── curves.py
│   │   │   ├── png_renderer.py
│   │   │   └── rich_renderer.py
│   │   ├── .gitkeep
│   │   ├── __init__.py
│   │   ├── advanced_analysis_criteria.py
│   │   ├── advanced_vision_module.py
│   │   ├── complete_validation_integration.py
│   │   ├── complete_vision_system.py
│   │   ├── cost_manager.py
│   │   ├── gabriel_image_interface.py
│   │   ├── gabriel_llm_integration_cache.py
│   │   ├── gabriel_llm_integration_safe.py
│   │   ├── gabriel_llm_integration_v2.py
│   │   ├── gabriel_vision_integration.py
│   │   ├── hol4_gap_mixed_generator.py
│   │   ├── hol_isabelle_formal_generator.py
│   │   ├── hol_lean_interface.py
│   │   ├── hol_proof_corrector.py
│   │   ├── image_access_manager.py
│   │   ├── image_discovery_system.py
│   │   ├── isabelle_validator.py
│   │   ├── llm_router.py
│   │   ├── llm_router_cache_extension.py
│   │   ├── llm_router_v2.py
│   │   ├── mathematical_engine.py
│   │   ├── parametric_validation_module.py
│   │   ├── pdf_rag_processor.py
│   │   ├── production_validation_system.py
│   │   ├── prompt_cache_manager.py
│   │   ├── prompt_injector.py
│   │   ├── validation_hol_knowledge.py
│   │   └── vision_module.py
│   ├── tests
│   │   ├── .gitkeep
│   │   ├── conftest.py
│   │   ├── test_adaptive_scale_v336.py
│   │   ├── test_ask_gabriel.py
│   │   ├── test_audit_store.py
│   │   ├── test_auto_graphs_nl_and_chaos_savard_trigger.py
│   │   ├── test_auto_trigger.py
│   │   ├── test_auto_trigger_conversational_context.py
│   │   ├── test_auto_trigger_opinion_context_v330.py
│   │   ├── test_banque_qr_sentinelle.py
│   │   ├── test_bloc_chaotique_ordonne_v330.py
│   │   ├── test_blocs_v343.py
│   │   ├── test_cartouche_uniforme_ascii.py
│   │   ├── test_certainty_model_and_logical_loop.py
│   │   ├── test_chaos_savard_and_question_graphs.py
│   │   ├── test_ci_regex_and_env_placeholder_fix.py
│   │   ├── test_ci_status.py
│   │   ├── test_cognitive.py
│   │   ├── test_composite_absurdity.py
│   │   ├── test_conversation_libre_savard.py
│   │   ├── test_conversational_memory.py
│   │   ├── test_conversational_memory_e2e.py
│   │   ├── test_conversational_mode.py
│   │   ├── test_critic_vocab_and_gestionnaire_fix.py
│   │   ├── test_debat_orchestrator.py
│   │   ├── test_debug_session.py
│   │   ├── test_debug_toolkit.py
│   │   ├── test_dictionnaire_rag.py
│   │   ├── test_dictionnaire_rag_bq_integration.py
│   │   ├── test_digamma_pure_v338.py
│   │   ├── test_domaine_sommes_XIA_v339.py
│   │   ├── test_engine_bridge.py
│   │   ├── test_env_config.py
│   │   ├── test_extract_numbers_unicode_v346.py
│   │   ├── test_filesystem_access.py
│   │   ├── test_forbidden_vocab_centralized.py
│   │   ├── test_gabriel_certification.py
│   │   ├── test_gabriel_v52_hol_formal.py
│   │   ├── test_gap_compute.py
│   │   ├── test_gap_solver_mixed_negative_positive.py
│   │   ├── test_generic_prime_i_query.py
│   │   ├── test_geometrie_spectrale_engine.py
│   │   ├── test_geometrie_tex_pasj02_fix.py
│   │   ├── test_graph_enrichment_v325.py
│   │   ├── test_image_command_windows_routing.py
│   │   ├── test_integrateur_memoire_api_fix.py
│   │   ├── test_isabelle_fixes_bugs_9_10.py
│   │   ├── test_isabelle_fixes_v321.py
│   │   ├── test_isabelle_rsp_non_zero_witness.py
│   │   ├── test_keybindings.py
│   │   ├── test_latex_healthcheck.py
│   │   ├── test_lean_methode_spectrale_port.py
│   │   ├── test_llm_reformulator.py
│   │   ├── test_logging_setup_esthetique.py
│   │   ├── test_mandatory_questions.py
│   │   ├── test_methode_spectral_healthcheck.py
│   │   ├── test_paths_resolution_container_fix.py
│   │   ├── test_philippe_three_categories_v329.py
│   │   ├── test_pipeline_epistemic.py
│   │   ├── test_plan_trifocal.py
│   │   ├── test_pre_reasoner_v334.py
│   │   ├── test_psi_savard_pont_zeta_v331.py
│   │   ├── test_psi_savard_v340.py
│   │   ├── test_restore_methode_spectral_0f277b5.py
│   │   ├── test_rsp_command.py
│   │   ├── test_rsp_curve.py
│   │   ├── test_section_XI_XII_integration.py
│   │   ├── test_section_xiii_professionnelle_v332.py
│   │   ├── test_section_xiii_rag_v333.py
│   │   ├── test_silent_audit.py
│   │   ├── test_slow_motion_debugger.py
│   │   ├── test_slow_motion_improvements.py
│   │   ├── test_spectral_family_foundations_v335.py
│   │   ├── test_spectral_ratio_configurations.py
│   │   ├── test_splash_and_citations.py
│   │   ├── test_timeout_and_extensions_v320.py
│   │   ├── test_traced_calculations.py
│   │   ├── test_ui_pro_banner_and_memoire.py
│   │   ├── test_unicode_surrogate_fix.py
│   │   ├── test_validation16_savard_and_build_workflow.py
│   │   ├── test_verification_loop.py
│   │   ├── test_verify_thy_structure.py
│   │   ├── test_visualization.py
│   │   ├── test_workflow_2025_2_contract.py
│   │   └── test_workflow_isabelle_syntax.py
│   ├── theories
│   │   ├── archive
│   │   │   └── methode_spectral_axiome_geometrique.thy
│   │   ├── banque_qr
│   │   │   └── QR_Technique_Spectre_Nombres_Premiers (1).pdf
│   │   ├── projects
│   │   │   ├── config
│   │   │   │   ├── config_savard_01.yml
│   │   │   │   ├── config_savard_02.yml
│   │   │   │   ├── config_savard_03.yml
│   │   │   │   ├── config_savard_04.yml
│   │   │   │   ├── config_savard_05.yml
│   │   │   │   ├── config_savard_06.yml
│   │   │   │   ├── config_savard_07.yml
│   │   │   │   ├── config_savard_08.yml
│   │   │   │   ├── config_savard_09.yml
│   │   │   │   └── config_savard_10.yml
│   │   │   ├── dot
│   │   │   │   ├── graphe_savard_01.dot
│   │   │   │   ├── graphe_savard_02.dot
│   │   │   │   ├── graphe_savard_03.dot
│   │   │   │   ├── graphe_savard_04.dot
│   │   │   │   ├── graphe_savard_05.dot
│   │   │   │   ├── graphe_savard_06.dot
│   │   │   │   ├── graphe_savard_07.dot
│   │   │   │   ├── graphe_savard_08.dot
│   │   │   │   ├── graphe_savard_09.dot
│   │   │   │   └── graphe_savard_10.dot
│   │   │   ├── lean
│   │   │   │   ├── lakefile.lean
│   │   │   │   ├── lean-toolchain
│   │   │   │   ├── Slot01.lean
│   │   │   │   ├── Slot02.lean
│   │   │   │   ├── Slot03.lean
│   │   │   │   ├── Slot04.lean
│   │   │   │   ├── Slot05.lean
│   │   │   │   ├── Slot06.lean
│   │   │   │   ├── Slot07.lean
│   │   │   │   ├── Slot08.lean
│   │   │   │   ├── Slot09.lean
│   │   │   │   ├── Slot10.lean
│   │   │   │   ├── Slot11.lean
│   │   │   │   ├── Slot12.lean
│   │   │   │   ├── Slot13.lean
│   │   │   │   ├── Slot14.lean
│   │   │   │   ├── Slot15.lean
│   │   │   │   ├── Slot16.lean
│   │   │   │   ├── Slot17.lean
│   │   │   │   ├── Slot18.lean
│   │   │   │   ├── Slot19.lean
│   │   │   │   ├── Slot20.lean
│   │   │   │   ├── Slot21.lean
│   │   │   │   ├── Slot22.lean
│   │   │   │   ├── Slot23.lean
│   │   │   │   ├── Slot24.lean
│   │   │   │   └── Slot25.lean
│   │   │   ├── md
│   │   │   │   ├── note_savard_01.md
│   │   │   │   ├── note_savard_02.md
│   │   │   │   ├── note_savard_03.md
│   │   │   │   ├── note_savard_04.md
│   │   │   │   ├── note_savard_05.md
│   │   │   │   ├── note_savard_06.md
│   │   │   │   ├── note_savard_07.md
│   │   │   │   ├── note_savard_08.md
│   │   │   │   ├── note_savard_09.md
│   │   │   │   ├── note_savard_10.md
│   │   │   │   ├── note_savard_11.md
│   │   │   │   ├── note_savard_12.md
│   │   │   │   ├── note_savard_13.md
│   │   │   │   ├── note_savard_14.md
│   │   │   │   ├── note_savard_15.md
│   │   │   │   ├── note_savard_16.md
│   │   │   │   ├── note_savard_17.md
│   │   │   │   ├── note_savard_18.md
│   │   │   │   ├── note_savard_19.md
│   │   │   │   ├── note_savard_20.md
│   │   │   │   ├── note_savard_21.md
│   │   │   │   ├── note_savard_22.md
│   │   │   │   ├── note_savard_23.md
│   │   │   │   ├── note_savard_24.md
│   │   │   │   ├── note_savard_25.md
│   │   │   │   ├── note_savard_26.md
│   │   │   │   ├── note_savard_27.md
│   │   │   │   ├── note_savard_28.md
│   │   │   │   ├── note_savard_29.md
│   │   │   │   ├── note_savard_30.md
│   │   │   │   ├── note_savard_31.md
│   │   │   │   ├── note_savard_32.md
│   │   │   │   ├── note_savard_33.md
│   │   │   │   ├── note_savard_34.md
│   │   │   │   ├── note_savard_35.md
│   │   │   │   ├── note_savard_36.md
│   │   │   │   ├── note_savard_37.md
│   │   │   │   ├── note_savard_38.md
│   │   │   │   ├── note_savard_39.md
│   │   │   │   ├── note_savard_40.md
│   │   │   │   ├── note_savard_41.md
│   │   │   │   ├── note_savard_42.md
│   │   │   │   ├── note_savard_43.md
│   │   │   │   ├── note_savard_44.md
│   │   │   │   ├── note_savard_45.md
│   │   │   │   ├── note_savard_46.md
│   │   │   │   ├── note_savard_47.md
│   │   │   │   ├── note_savard_48.md
│   │   │   │   ├── note_savard_49.md
│   │   │   │   └── note_savard_50.md
│   │   │   ├── notebooks
│   │   │   │   ├── notebook_savard_01.ipynb
│   │   │   │   ├── notebook_savard_02.ipynb
│   │   │   │   ├── notebook_savard_03.ipynb
│   │   │   │   ├── notebook_savard_04.ipynb
│   │   │   │   ├── notebook_savard_05.ipynb
│   │   │   │   ├── notebook_savard_06.ipynb
│   │   │   │   ├── notebook_savard_07.ipynb
│   │   │   │   ├── notebook_savard_08.ipynb
│   │   │   │   ├── notebook_savard_09.ipynb
│   │   │   │   └── notebook_savard_10.ipynb
│   │   │   ├── py
│   │   │   │   ├── analyse_savard_01.py
│   │   │   │   ├── analyse_savard_02.py
│   │   │   │   ├── analyse_savard_03.py
│   │   │   │   ├── analyse_savard_04.py
│   │   │   │   ├── analyse_savard_05.py
│   │   │   │   ├── analyse_savard_06.py
│   │   │   │   ├── analyse_savard_07.py
│   │   │   │   ├── analyse_savard_08.py
│   │   │   │   ├── analyse_savard_09.py
│   │   │   │   ├── analyse_savard_10.py
│   │   │   │   ├── analyse_savard_11.py
│   │   │   │   ├── analyse_savard_12.py
│   │   │   │   ├── analyse_savard_13.py
│   │   │   │   ├── analyse_savard_14.py
│   │   │   │   ├── analyse_savard_15.py
│   │   │   │   ├── analyse_savard_16.py
│   │   │   │   ├── analyse_savard_17.py
│   │   │   │   ├── analyse_savard_18.py
│   │   │   │   ├── analyse_savard_19.py
│   │   │   │   ├── analyse_savard_20.py
│   │   │   │   ├── analyse_savard_21.py
│   │   │   │   ├── analyse_savard_22.py
│   │   │   │   ├── analyse_savard_23.py
│   │   │   │   ├── analyse_savard_24.py
│   │   │   │   └── analyse_savard_25.py
│   │   │   ├── roots
│   │   │   │   ├── session_01
│   │   │   │   │   └── ROOT
│   │   │   │   ├── session_02
│   │   │   │   │   └── ROOT
│   │   │   │   ├── session_03
│   │   │   │   │   └── ROOT
│   │   │   │   ├── session_04
│   │   │   │   │   └── ROOT
│   │   │   │   ├── session_05
│   │   │   │   │   └── ROOT
│   │   │   │   ├── session_06
│   │   │   │   │   └── ROOT
│   │   │   │   ├── session_07
│   │   │   │   │   └── ROOT
│   │   │   │   ├── session_08
│   │   │   │   │   └── ROOT
│   │   │   │   ├── session_09
│   │   │   │   │   └── ROOT
│   │   │   │   ├── session_10
│   │   │   │   │   └── ROOT
│   │   │   │   ├── session_11
│   │   │   │   │   └── ROOT
│   │   │   │   ├── session_12
│   │   │   │   │   └── ROOT
│   │   │   │   ├── session_13
│   │   │   │   │   └── ROOT
│   │   │   │   ├── session_14
│   │   │   │   │   └── ROOT
│   │   │   │   ├── session_15
│   │   │   │   │   └── ROOT
│   │   │   │   ├── session_16
│   │   │   │   │   └── ROOT
│   │   │   │   ├── session_17
│   │   │   │   │   └── ROOT
│   │   │   │   ├── session_18
│   │   │   │   │   └── ROOT
│   │   │   │   ├── session_19
│   │   │   │   │   └── ROOT
│   │   │   │   ├── session_20
│   │   │   │   │   └── ROOT
│   │   │   │   ├── session_21
│   │   │   │   │   └── ROOT
│   │   │   │   ├── session_22
│   │   │   │   │   └── ROOT
│   │   │   │   ├── session_23
│   │   │   │   │   └── ROOT
│   │   │   │   ├── session_24
│   │   │   │   │   └── ROOT
│   │   │   │   └── session_25
│   │   │   │       └── ROOT
│   │   │   ├── scripts
│   │   │   │   ├── script_savard_01.sh
│   │   │   │   ├── script_savard_02.sh
│   │   │   │   ├── script_savard_03.sh
│   │   │   │   ├── script_savard_04.sh
│   │   │   │   ├── script_savard_05.sh
│   │   │   │   ├── script_savard_06.sh
│   │   │   │   ├── script_savard_07.sh
│   │   │   │   ├── script_savard_08.sh
│   │   │   │   ├── script_savard_09.sh
│   │   │   │   └── script_savard_10.sh
│   │   │   ├── svg
│   │   │   │   ├── schema_savard_01.svg
│   │   │   │   ├── schema_savard_02.svg
│   │   │   │   ├── schema_savard_03.svg
│   │   │   │   ├── schema_savard_04.svg
│   │   │   │   ├── schema_savard_05.svg
│   │   │   │   ├── schema_savard_06.svg
│   │   │   │   ├── schema_savard_07.svg
│   │   │   │   ├── schema_savard_08.svg
│   │   │   │   ├── schema_savard_09.svg
│   │   │   │   └── schema_savard_10.svg
│   │   │   ├── tex
│   │   │   │   ├── biblio_savard_01.bib
│   │   │   │   ├── biblio_savard_02.bib
│   │   │   │   ├── biblio_savard_03.bib
│   │   │   │   ├── biblio_savard_04.bib
│   │   │   │   ├── biblio_savard_05.bib
│   │   │   │   ├── biblio_savard_06.bib
│   │   │   │   ├── biblio_savard_07.bib
│   │   │   │   ├── biblio_savard_08.bib
│   │   │   │   ├── biblio_savard_09.bib
│   │   │   │   ├── biblio_savard_10.bib
│   │   │   │   ├── projet_uni_car_savard_01.tex
│   │   │   │   ├── projet_uni_car_savard_02.tex
│   │   │   │   ├── projet_uni_car_savard_03.tex
│   │   │   │   ├── projet_uni_car_savard_04.tex
│   │   │   │   ├── projet_uni_car_savard_05.tex
│   │   │   │   ├── projet_uni_car_savard_06.tex
│   │   │   │   ├── projet_uni_car_savard_07.tex
│   │   │   │   ├── projet_uni_car_savard_08.tex
│   │   │   │   ├── projet_uni_car_savard_09.tex
│   │   │   │   ├── projet_uni_car_savard_10.tex
│   │   │   │   ├── projet_uni_car_savard_100.tex
│   │   │   │   ├── projet_uni_car_savard_11.tex
│   │   │   │   ├── projet_uni_car_savard_12.tex
│   │   │   │   ├── projet_uni_car_savard_13.tex
│   │   │   │   ├── projet_uni_car_savard_14.tex
│   │   │   │   ├── projet_uni_car_savard_15.tex
│   │   │   │   ├── projet_uni_car_savard_16.tex
│   │   │   │   ├── projet_uni_car_savard_17.tex
│   │   │   │   ├── projet_uni_car_savard_18.tex
│   │   │   │   ├── projet_uni_car_savard_19.tex
│   │   │   │   ├── projet_uni_car_savard_20.tex
│   │   │   │   ├── projet_uni_car_savard_21.tex
│   │   │   │   ├── projet_uni_car_savard_22.tex
│   │   │   │   ├── projet_uni_car_savard_23.tex
│   │   │   │   ├── projet_uni_car_savard_24.tex
│   │   │   │   ├── projet_uni_car_savard_25.tex
│   │   │   │   ├── projet_uni_car_savard_26.tex
│   │   │   │   ├── projet_uni_car_savard_27.tex
│   │   │   │   ├── projet_uni_car_savard_28.tex
│   │   │   │   ├── projet_uni_car_savard_29.tex
│   │   │   │   ├── projet_uni_car_savard_30.tex
│   │   │   │   ├── projet_uni_car_savard_31.tex
│   │   │   │   ├── projet_uni_car_savard_32.tex
│   │   │   │   ├── projet_uni_car_savard_33.tex
│   │   │   │   ├── projet_uni_car_savard_34.tex
│   │   │   │   ├── projet_uni_car_savard_35.tex
│   │   │   │   ├── projet_uni_car_savard_36.tex
│   │   │   │   ├── projet_uni_car_savard_37.tex
│   │   │   │   ├── projet_uni_car_savard_38.tex
│   │   │   │   ├── projet_uni_car_savard_39.tex
│   │   │   │   ├── projet_uni_car_savard_40.tex
│   │   │   │   ├── projet_uni_car_savard_41.tex
│   │   │   │   ├── projet_uni_car_savard_42.tex
│   │   │   │   ├── projet_uni_car_savard_43.tex
│   │   │   │   ├── projet_uni_car_savard_44.tex
│   │   │   │   ├── projet_uni_car_savard_45.tex
│   │   │   │   ├── projet_uni_car_savard_46.tex
│   │   │   │   ├── projet_uni_car_savard_47.tex
│   │   │   │   ├── projet_uni_car_savard_48.tex
│   │   │   │   ├── projet_uni_car_savard_49.tex
│   │   │   │   ├── projet_uni_car_savard_50.tex
│   │   │   │   ├── projet_uni_car_savard_51.tex
│   │   │   │   ├── projet_uni_car_savard_52.tex
│   │   │   │   ├── projet_uni_car_savard_53.tex
│   │   │   │   ├── projet_uni_car_savard_54.tex
│   │   │   │   ├── projet_uni_car_savard_55.tex
│   │   │   │   ├── projet_uni_car_savard_56.tex
│   │   │   │   ├── projet_uni_car_savard_57.tex
│   │   │   │   ├── projet_uni_car_savard_58.tex
│   │   │   │   ├── projet_uni_car_savard_59.tex
│   │   │   │   ├── projet_uni_car_savard_60.tex
│   │   │   │   ├── projet_uni_car_savard_61.tex
│   │   │   │   ├── projet_uni_car_savard_62.tex
│   │   │   │   ├── projet_uni_car_savard_63.tex
│   │   │   │   ├── projet_uni_car_savard_64.tex
│   │   │   │   ├── projet_uni_car_savard_65.tex
│   │   │   │   ├── projet_uni_car_savard_66.tex
│   │   │   │   ├── projet_uni_car_savard_67.tex
│   │   │   │   ├── projet_uni_car_savard_68.tex
│   │   │   │   ├── projet_uni_car_savard_69.tex
│   │   │   │   ├── projet_uni_car_savard_70.tex
│   │   │   │   ├── projet_uni_car_savard_71.tex
│   │   │   │   ├── projet_uni_car_savard_72.tex
│   │   │   │   ├── projet_uni_car_savard_73.tex
│   │   │   │   ├── projet_uni_car_savard_74.tex
│   │   │   │   ├── projet_uni_car_savard_75.tex
│   │   │   │   ├── projet_uni_car_savard_76.tex
│   │   │   │   ├── projet_uni_car_savard_77.tex
│   │   │   │   ├── projet_uni_car_savard_78.tex
│   │   │   │   ├── projet_uni_car_savard_79.tex
│   │   │   │   ├── projet_uni_car_savard_80.tex
│   │   │   │   ├── projet_uni_car_savard_81.tex
│   │   │   │   ├── projet_uni_car_savard_82.tex
│   │   │   │   ├── projet_uni_car_savard_83.tex
│   │   │   │   ├── projet_uni_car_savard_84.tex
│   │   │   │   ├── projet_uni_car_savard_85.tex
│   │   │   │   ├── projet_uni_car_savard_86.tex
│   │   │   │   ├── projet_uni_car_savard_87.tex
│   │   │   │   ├── projet_uni_car_savard_88.tex
│   │   │   │   ├── projet_uni_car_savard_89.tex
│   │   │   │   ├── projet_uni_car_savard_90.tex
│   │   │   │   ├── projet_uni_car_savard_91.tex
│   │   │   │   ├── projet_uni_car_savard_92.tex
│   │   │   │   ├── projet_uni_car_savard_93.tex
│   │   │   │   ├── projet_uni_car_savard_94.tex
│   │   │   │   ├── projet_uni_car_savard_95.tex
│   │   │   │   ├── projet_uni_car_savard_96.tex
│   │   │   │   ├── projet_uni_car_savard_97.tex
│   │   │   │   ├── projet_uni_car_savard_98.tex
│   │   │   │   └── projet_uni_car_savard_99.tex
│   │   │   ├── txt
│   │   │   │   ├── Géométrie du Spectre des Nombres Premiers — Brouillon Conceptuel Savard 2026.pdf
│   │   │   │   ├── projet_uni_car_savard_01.txt
│   │   │   │   ├── projet_uni_car_savard_02.txt
│   │   │   │   ├── projet_uni_car_savard_03.txt
│   │   │   │   ├── projet_uni_car_savard_04.txt
│   │   │   │   ├── projet_uni_car_savard_05.txt
│   │   │   │   ├── projet_uni_car_savard_06.txt
│   │   │   │   ├── projet_uni_car_savard_07.txt
│   │   │   │   ├── projet_uni_car_savard_08.txt
│   │   │   │   ├── projet_uni_car_savard_09.txt
│   │   │   │   ├── projet_uni_car_savard_10.txt
│   │   │   │   ├── projet_uni_car_savard_100.txt
│   │   │   │   ├── projet_uni_car_savard_11.txt
│   │   │   │   ├── projet_uni_car_savard_12.txt
│   │   │   │   ├── projet_uni_car_savard_13.txt
│   │   │   │   ├── projet_uni_car_savard_14.txt
│   │   │   │   ├── projet_uni_car_savard_15.txt
│   │   │   │   ├── projet_uni_car_savard_16.txt
│   │   │   │   ├── projet_uni_car_savard_17.txt
│   │   │   │   ├── projet_uni_car_savard_18.txt
│   │   │   │   ├── projet_uni_car_savard_19.txt
│   │   │   │   ├── projet_uni_car_savard_20.txt
│   │   │   │   ├── projet_uni_car_savard_21.txt
│   │   │   │   ├── projet_uni_car_savard_22.txt
│   │   │   │   ├── projet_uni_car_savard_23.txt
│   │   │   │   ├── projet_uni_car_savard_24.txt
│   │   │   │   ├── projet_uni_car_savard_25.txt
│   │   │   │   ├── projet_uni_car_savard_26.txt
│   │   │   │   ├── projet_uni_car_savard_27.txt
│   │   │   │   ├── projet_uni_car_savard_28.txt
│   │   │   │   ├── projet_uni_car_savard_29.txt
│   │   │   │   ├── projet_uni_car_savard_30.txt
│   │   │   │   ├── projet_uni_car_savard_31.txt
│   │   │   │   ├── projet_uni_car_savard_32.txt
│   │   │   │   ├── projet_uni_car_savard_33.txt
│   │   │   │   ├── projet_uni_car_savard_34.txt
│   │   │   │   ├── projet_uni_car_savard_35.txt
│   │   │   │   ├── projet_uni_car_savard_36.txt
│   │   │   │   ├── projet_uni_car_savard_37.txt
│   │   │   │   ├── projet_uni_car_savard_38.txt
│   │   │   │   ├── projet_uni_car_savard_39.txt
│   │   │   │   ├── projet_uni_car_savard_40.txt
│   │   │   │   ├── projet_uni_car_savard_41.txt
│   │   │   │   ├── projet_uni_car_savard_42.txt
│   │   │   │   ├── projet_uni_car_savard_43.txt
│   │   │   │   ├── projet_uni_car_savard_44.txt
│   │   │   │   ├── projet_uni_car_savard_45.txt
│   │   │   │   ├── projet_uni_car_savard_46.txt
│   │   │   │   ├── projet_uni_car_savard_47.txt
│   │   │   │   ├── projet_uni_car_savard_48.txt
│   │   │   │   ├── projet_uni_car_savard_49.txt
│   │   │   │   ├── projet_uni_car_savard_50.txt
│   │   │   │   ├── projet_uni_car_savard_51.txt
│   │   │   │   ├── projet_uni_car_savard_52.txt
│   │   │   │   ├── projet_uni_car_savard_53.txt
│   │   │   │   ├── projet_uni_car_savard_54.txt
│   │   │   │   ├── projet_uni_car_savard_55.txt
│   │   │   │   ├── projet_uni_car_savard_56.txt
│   │   │   │   ├── projet_uni_car_savard_57.txt
│   │   │   │   ├── projet_uni_car_savard_58.txt
│   │   │   │   ├── projet_uni_car_savard_59.txt
│   │   │   │   ├── projet_uni_car_savard_60.txt
│   │   │   │   ├── projet_uni_car_savard_61.txt
│   │   │   │   ├── projet_uni_car_savard_62.txt
│   │   │   │   ├── projet_uni_car_savard_63.txt
│   │   │   │   ├── projet_uni_car_savard_64.txt
│   │   │   │   ├── projet_uni_car_savard_65.txt
│   │   │   │   ├── projet_uni_car_savard_66.txt
│   │   │   │   ├── projet_uni_car_savard_67.txt
│   │   │   │   ├── projet_uni_car_savard_68.txt
│   │   │   │   ├── projet_uni_car_savard_69.txt
│   │   │   │   ├── projet_uni_car_savard_70.txt
│   │   │   │   ├── projet_uni_car_savard_71.txt
│   │   │   │   ├── projet_uni_car_savard_72.txt
│   │   │   │   ├── projet_uni_car_savard_73.txt
│   │   │   │   ├── projet_uni_car_savard_74.txt
│   │   │   │   ├── projet_uni_car_savard_75.txt
│   │   │   │   ├── projet_uni_car_savard_76.txt
│   │   │   │   ├── projet_uni_car_savard_77.txt
│   │   │   │   ├── projet_uni_car_savard_78.txt
│   │   │   │   ├── projet_uni_car_savard_79.txt
│   │   │   │   ├── projet_uni_car_savard_80.txt
│   │   │   │   ├── projet_uni_car_savard_81.txt
│   │   │   │   ├── projet_uni_car_savard_82.txt
│   │   │   │   ├── projet_uni_car_savard_83.txt
│   │   │   │   ├── projet_uni_car_savard_84.txt
│   │   │   │   ├── projet_uni_car_savard_85.txt
│   │   │   │   ├── projet_uni_car_savard_86.txt
│   │   │   │   ├── projet_uni_car_savard_87.txt
│   │   │   │   ├── projet_uni_car_savard_88.txt
│   │   │   │   ├── projet_uni_car_savard_89.txt
│   │   │   │   ├── projet_uni_car_savard_90.txt
│   │   │   │   ├── projet_uni_car_savard_91.txt
│   │   │   │   ├── projet_uni_car_savard_92.txt
│   │   │   │   ├── projet_uni_car_savard_93.txt
│   │   │   │   ├── projet_uni_car_savard_94.txt
│   │   │   │   ├── projet_uni_car_savard_95.txt
│   │   │   │   ├── projet_uni_car_savard_96.txt
│   │   │   │   ├── projet_uni_car_savard_97.txt
│   │   │   │   ├── projet_uni_car_savard_98.txt
│   │   │   │   └── projet_uni_car_savard_99.txt
│   │   │   ├── projet_uni_car_savard_01.thy
│   │   │   ├── projet_uni_car_savard_02.thy
│   │   │   ├── projet_uni_car_savard_03.thy
│   │   │   ├── projet_uni_car_savard_04.thy
│   │   │   ├── projet_uni_car_savard_05.thy
│   │   │   ├── projet_uni_car_savard_06.thy
│   │   │   ├── projet_uni_car_savard_07.thy
│   │   │   ├── projet_uni_car_savard_08.thy
│   │   │   ├── projet_uni_car_savard_09.thy
│   │   │   ├── projet_uni_car_savard_10.thy
│   │   │   ├── projet_uni_car_savard_100.thy
│   │   │   ├── projet_uni_car_savard_11.thy
│   │   │   ├── projet_uni_car_savard_12.thy
│   │   │   ├── projet_uni_car_savard_13.thy
│   │   │   ├── projet_uni_car_savard_14.thy
│   │   │   ├── projet_uni_car_savard_15.thy
│   │   │   ├── projet_uni_car_savard_16.thy
│   │   │   ├── projet_uni_car_savard_17.thy
│   │   │   ├── projet_uni_car_savard_18.thy
│   │   │   ├── projet_uni_car_savard_19.thy
│   │   │   ├── projet_uni_car_savard_20.thy
│   │   │   ├── projet_uni_car_savard_21.thy
│   │   │   ├── projet_uni_car_savard_22.thy
│   │   │   ├── projet_uni_car_savard_23.thy
│   │   │   ├── projet_uni_car_savard_24.thy
│   │   │   ├── projet_uni_car_savard_25.thy
│   │   │   ├── projet_uni_car_savard_26.thy
│   │   │   ├── projet_uni_car_savard_27.thy
│   │   │   ├── projet_uni_car_savard_28.thy
│   │   │   ├── projet_uni_car_savard_29.thy
│   │   │   ├── projet_uni_car_savard_30.thy
│   │   │   ├── projet_uni_car_savard_31.thy
│   │   │   ├── projet_uni_car_savard_32.thy
│   │   │   ├── projet_uni_car_savard_33.thy
│   │   │   ├── projet_uni_car_savard_34.thy
│   │   │   ├── projet_uni_car_savard_35.thy
│   │   │   ├── projet_uni_car_savard_36.thy
│   │   │   ├── projet_uni_car_savard_37.thy
│   │   │   ├── projet_uni_car_savard_38.thy
│   │   │   ├── projet_uni_car_savard_39.thy
│   │   │   ├── projet_uni_car_savard_40.thy
│   │   │   ├── projet_uni_car_savard_41.thy
│   │   │   ├── projet_uni_car_savard_42.thy
│   │   │   ├── projet_uni_car_savard_43.thy
│   │   │   ├── projet_uni_car_savard_44.thy
│   │   │   ├── projet_uni_car_savard_45.thy
│   │   │   ├── projet_uni_car_savard_46.thy
│   │   │   ├── projet_uni_car_savard_47.thy
│   │   │   ├── projet_uni_car_savard_48.thy
│   │   │   ├── projet_uni_car_savard_49.thy
│   │   │   ├── projet_uni_car_savard_50.thy
│   │   │   ├── projet_uni_car_savard_51.thy
│   │   │   ├── projet_uni_car_savard_52.thy
│   │   │   ├── projet_uni_car_savard_53.thy
│   │   │   ├── projet_uni_car_savard_54.thy
│   │   │   ├── projet_uni_car_savard_55.thy
│   │   │   ├── projet_uni_car_savard_56.thy
│   │   │   ├── projet_uni_car_savard_57.thy
│   │   │   ├── projet_uni_car_savard_58.thy
│   │   │   ├── projet_uni_car_savard_59.thy
│   │   │   ├── projet_uni_car_savard_60.thy
│   │   │   ├── projet_uni_car_savard_61.thy
│   │   │   ├── projet_uni_car_savard_62.thy
│   │   │   ├── projet_uni_car_savard_63.thy
│   │   │   ├── projet_uni_car_savard_64.thy
│   │   │   ├── projet_uni_car_savard_65.thy
│   │   │   ├── projet_uni_car_savard_66.thy
│   │   │   ├── projet_uni_car_savard_67.thy
│   │   │   ├── projet_uni_car_savard_68.thy
│   │   │   ├── projet_uni_car_savard_69.thy
│   │   │   ├── projet_uni_car_savard_70.thy
│   │   │   ├── projet_uni_car_savard_71.thy
│   │   │   ├── projet_uni_car_savard_72.thy
│   │   │   ├── projet_uni_car_savard_73.thy
│   │   │   ├── projet_uni_car_savard_74.thy
│   │   │   ├── projet_uni_car_savard_75.thy
│   │   │   ├── projet_uni_car_savard_76.thy
│   │   │   ├── projet_uni_car_savard_77.thy
│   │   │   ├── projet_uni_car_savard_78.thy
│   │   │   ├── projet_uni_car_savard_79.thy
│   │   │   ├── projet_uni_car_savard_80.thy
│   │   │   ├── projet_uni_car_savard_81.thy
│   │   │   ├── projet_uni_car_savard_82.thy
│   │   │   ├── projet_uni_car_savard_83.thy
│   │   │   ├── projet_uni_car_savard_84.thy
│   │   │   ├── projet_uni_car_savard_85.thy
│   │   │   ├── projet_uni_car_savard_86.thy
│   │   │   ├── projet_uni_car_savard_87.thy
│   │   │   ├── projet_uni_car_savard_88.thy
│   │   │   ├── projet_uni_car_savard_89.thy
│   │   │   ├── projet_uni_car_savard_90.thy
│   │   │   ├── projet_uni_car_savard_91.thy
│   │   │   ├── projet_uni_car_savard_92.thy
│   │   │   ├── projet_uni_car_savard_93.thy
│   │   │   ├── projet_uni_car_savard_94.thy
│   │   │   ├── projet_uni_car_savard_95.thy
│   │   │   ├── projet_uni_car_savard_96.thy
│   │   │   ├── projet_uni_car_savard_97.thy
│   │   │   ├── projet_uni_car_savard_98.thy
│   │   │   └── projet_uni_car_savard_99.thy
│   │   ├── tex
│   │   │   ├── archives
│   │   │   │   ├── geometrie_du_spectre_des_nombres_premiers.pdf
│   │   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_aout_08_2026.pdf
│   │   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.aux
│   │   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.aux
│   │   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.listing
│   │   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.log
│   │   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.out
│   │   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.pdf
│   │   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex
│   │   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.toc
│   │   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.listing
│   │   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.log
│   │   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.out
│   │   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.pdf
│   │   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json
│   │   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json
│   │   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.toc
│   │   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026_styled.log
│   │   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026_styled.pdf
│   │   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026_styled_v2.log
│   │   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026_styled_v2.pdf
│   │   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026_styled_v3.log
│   │   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026_styled_v3.pdf
│   │   │   │   └── texput.log
│   │   │   ├── PDF
│   │   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers.pdf
│   │   │   │   └── README_pdf.txt
│   │   │   ├── qa_output
│   │   │   ├── tex_quality
│   │   │   │   ├── quality_pipeline.py
│   │   │   │   ├── README.md
│   │   │   │   ├── style_profile.py
│   │   │   │   └── termbase_ca_qc.csv
│   │   │   ├── convert_docx_to_latex.py
│   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_2026.log
│   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_2026.pdf
│   │   │   ├── Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex
│   │   │   └── README_pdf.md
│   │   ├── Words_docx
│   │   │   └── Géométrie du Spectre des Nombres Premiers — Brouillon Savard 2026.docx
│   │   ├── geometrie_spectre_premier.thy
│   │   ├── methode_spectral.thy
│   │   ├── methode_spectral_de.thy
│   │   ├── methode_spectral_en.thy
│   │   ├── methode_spectral_es.thy
│   │   ├── methode_spectral_ja.thy
│   │   ├── methode_spectral_pt.thy
│   │   ├── methode_spectral_ru.thy
│   │   ├── methode_spectral_zh.thy
│   │   ├── MethodeSpectrale.lean
│   │   ├── PLAN_FACTORISATION_ET_META_THEORY.md
│   │   ├── README_LEAN.md
│   │   ├── RiemannSpectral.lean
│   │   ├── ROOT
│   │   ├── validation_hol_unifiee.thy
│   │   └── verify_thy_structure.py
│   ├── .dockerignore
│   ├── .gitignore
│   ├── 00_START_HERE_IMAGE_ANALYSIS.md
│   ├── apply_image_analysis_patch.py
│   ├── apply_optimization.py
│   ├── BUG_FIX_URGENT_HOL.md
│   ├── CHANGELOG.md
│   ├── CHECKLIST_FINAL.md
│   ├── CINEMATIC_DEPLOYMENT.md
│   ├── CINEMATIC_EXAMPLES.py
│   ├── CINEMATIC_INTEGRATION_GUIDE.md
│   ├── CINEMATIC_MODE_SUMMARY.md
│   ├── CLAUDE_BUDGET_GUIDE.md
│   ├── clean-docker.ps1
│   ├── cognitive_pipeline_hol_unified.py
│   ├── COMMANDES_PRATIQUES_ANALYSE.md
│   ├── COMMANDS_COMPLETE_REFERENCE.md
│   ├── COMPLETE_INTEGRATION_INSTRUCTIONS.md
│   ├── config.yaml
│   ├── CONFIG_ENV_GUIDE.md
│   ├── config_optimized.yaml
│   ├── COPIER_COLLER_DIRECT.py
│   ├── CORRECTION_ERREUR_TCHEBYCHEV_GABRIEL.md
│   ├── CORRECTION_RSA_v2.2.md
│   ├── deploy_image_analysis.py
│   ├── DEPLOYMENT_CHECKLIST_v4.0.md
│   ├── DEPLOYMENT_READY.txt
│   ├── DEPLOYMENT_SUMMARY.md
│   ├── docker-compose.yml
│   ├── Dockerfile.cli
│   ├── env.example.txt
│   ├── ETAPE5_AMELIORATIONS_PRIORITAIRES.md
│   ├── EXEMPLE_GABRIEL_v2.1.py
│   ├── FILES_v5.0.md
│   ├── FINAL_300_TEMPLATES_SUMMARY.md
│   ├── FINAL_RECONSTRUCTION_SUMMARY.txt
│   ├── gabriel.ps1
│   ├── GABRIEL_COMPLETE_VISION_INTEGRATION.md
│   ├── gabriel_control.py
│   ├── GABRIEL_DEBUGGER_PAUSE_STATUS.md
│   ├── GABRIEL_DOMAIN_SYSTEM_INTEGRATION_GUIDE.md
│   ├── GABRIEL_FINAL_SOLUTION.txt
│   ├── GABRIEL_FINAL_v5_SOCKET_CLEANUP.md
│   ├── GABRIEL_IMAGE_ANALYSIS_COMPLETE_GUIDE.md
│   ├── gabriel_launcher.py
│   ├── gabriel_mathematical.py
│   ├── GABRIEL_PARAMETRIC_VALIDATION_GUIDE.md
│   ├── GABRIEL_PERFORMANCE_OPTIMIZATION.md
│   ├── GABRIEL_PORT_FIX_v5.3.md
│   ├── GABRIEL_PRODUCTION_VALIDATION_GUIDE.md
│   ├── GABRIEL_v2.1_RELEASE_NOTES.md
│   ├── GABRIEL_v2.2_RSA_CAPABILITY.md
│   ├── GABRIEL_v3.0_MULTILOOP_VALIDATION.md
│   ├── GABRIEL_v4.0_THEORY_MEMORY.md
│   ├── GABRIEL_v5.0_FINAL_SUMMARY.txt
│   ├── GABRIEL_v5.0_LLM_ROUTING.md
│   ├── GABRIEL_v5.1_SAFE_BUDGET.md
│   ├── GABRIEL_v5.2_DEPLOYMENT_SUMMARY.md
│   ├── GABRIEL_v5.2_HOL_FORMAL.md
│   ├── GABRIEL_v5.4_WORKING_SOLUTION.md
│   ├── GABRIEL_v5_EXPLIQUE_SIMPLEMENT.txt
│   ├── GABRIEL_v5_UPDATE_GUIDE.md
│   ├── GABRIEL_VALIDATION_EXAMPLES.md
│   ├── GABRIEL_VISION_MODULE_DOCUMENTATION.md
│   ├── GABRIEL_VISION_QUICK_START.md
│   ├── GABRIEL_VISION_VERIFICATION_COMPLETE.md
│   ├── generate_thy_templates.py
│   ├── generate_txt_tex_templates.py
│   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.aux
│   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.listing
│   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.log
│   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.out
│   ├── Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.toc
│   ├── GO_QUICK_START.md
│   ├── GUIDE_ANALYSE_AVEC_CRITERES.md
│   ├── GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md
│   ├── GUIDE_JEDIT_GABRIEL.md
│   ├── GUIDE_RECONSTRUCTION_REDEMARRAGE.md
│   ├── HOL4_SYSTEMATIC_PROOFS.md
│   ├── HOL_ISABELLE_FIX.md
│   ├── IMAGE_ANALYSIS_ANSWER_DIRECT.md
│   ├── INDEX.md
│   ├── INTEGRATION_MANUELLE.py
│   ├── integration_mathematical.py
│   ├── INTEGRATION_PATCH_IMAGE_ANALYSIS.md
│   ├── INTEGRATION_UNIVERSESTAUCARRE.md
│   ├── JEDIT_QUICK_REFERENCE.md
│   ├── lakefile.lean
│   ├── lean-toolchain
│   ├── main.py
│   ├── main_cli.py
│   ├── MIGRATION_VALIDATION_SYSTEMS.md
│   ├── MOT_FIN_SESSION.txt
│   ├── MULTIFORMAT_TEMPLATES_GUIDE.md
│   ├── OPTIMIZATION_SUMMARY.md
│   ├── ORGANISATION_GUIDE_UTILISATEUR_COMPLETE.txt
│   ├── PATCH_IMAGE_ANALYSIS_INTEGRATION.py
│   ├── PATCH_THEORETICAL_RECOGNITION.md
│   ├── port-locker.ps1
│   ├── port_cleanup.py
│   ├── PORT_CLEANUP_IMPLEMENTATION.md
│   ├── POWERSHELL_ISE_GUIDE.md
│   ├── PROJECTS_TEMPLATES_GUIDE.md
│   ├── PYTEST_CHECKLIST.md
│   ├── PYTEST_EXECUTION_GUIDE.md
│   ├── PYTEST_INDEX.md
│   ├── PYTEST_LIST_COMPLETE.md
│   ├── PYTEST_SUMMARY.md
│   ├── question-definition.txt
│   ├── quick-start.sh
│   ├── QUICK_REFERENCE.md
│   ├── QUICK_START_5_MINUTES.md
│   ├── QUICK_START_IMAGE_ANALYSIS.md
│   ├── quick_verification.py
│   ├── RAPPORT_ANALYSE_DEPENDANCES.md
│   ├── RAPPORT_ETAPE1_ANALYSE_README.md
│   ├── RAPPORT_ETAPE2_ANALYSE_ARCHITECTURE.md
│   ├── RAPPORT_MAINTENANCE_ETAPE3.md
│   ├── README.md
│   ├── README_CINEMATIC_MODE.md
│   ├── README_FINAL_v5.4.md
│   ├── RELEASE_NOTES_v2.1.md
│   ├── RELEASE_v2.1_COMPLETE.txt
│   ├── REPONSE_OUI_PREUVES_HOL4_SYSTEMATIQUES.md
│   ├── REPONSE_RAPIDE_RECONSTRUCTION.md
│   ├── requirements.txt
│   ├── RESUME_SESSION_COMPLETE.md
│   ├── ROOT
│   ├── run-tests.bat
│   ├── run-tests.ps1
│   ├── SECURITY_FIXES_SUMMARY.md
│   ├── SETUP_MATHEMATICAL_v2.md
│   ├── SHORTCUTS_AND_TIPS.md
│   ├── socket_cleanup.py
│   ├── SOLUTION_FINALE.txt
│   ├── SOLUTION_SUMMARY_v5.3.txt
│   ├── start-agent.ps1
│   ├── START_GABRIEL.bat
│   ├── START_HERE.txt
│   ├── START_v5.0.txt
│   ├── STOP_GABRIEL.bat
│   ├── SYNTHESE_RSA_v2.2.md
│   ├── SYNTHESE_ULTIME_v2.1.md
│   ├── TEMPLATES_SUMMARY.md
│   ├── test-integration.sh
│   ├── test_rsa_capability.py
│   ├── test_spectral_gabriel.py
│   ├── TODO_ANALYSE.md
│   ├── UPDATE_GABRIEL_v5.ps1
│   ├── UTF8_ENCODING_FIX.md
│   ├── VALIDATION_HOL_INTEGRATION_COMPLETE.md
│   ├── VALIDATION_HOL_UNIFIEE_ANALYSIS.md
│   ├── VERIFICATION_COMPLETE_RESULTAT_FINAL.md
│   ├── VERIFICATION_FINALE_SYNTHESE.txt
│   └── VISUAL_SUMMARY_IMAGE_ANALYSIS.txt
├── backend
│   ├── requirements.txt
│   └── server.py
├── docs
│   ├── .nojekyll
│   ├── index.html
│   └── README.md
├── frontend
│   ├── plugins
│   │   └── health-check
│   │       ├── health-endpoints.js
│   │       └── webpack-health-plugin.js
│   ├── public
│   │   └── index.html
│   ├── src
│   │   ├── agent-local-ia-carre
│   │   │   ├── .gitconfig
│   │   │   ├── arbo.txt
│   │   │   └── yarn.lock
│   │   ├── components
│   │   │   └── ui
│   │   │       ├── accordion.jsx
│   │   │       ├── alert-dialog.jsx
│   │   │       ├── alert.jsx
│   │   │       ├── aspect-ratio.jsx
│   │   │       ├── avatar.jsx
│   │   │       ├── badge.jsx
│   │   │       ├── breadcrumb.jsx
│   │   │       ├── button.jsx
│   │   │       ├── calendar.jsx
│   │   │       ├── card.jsx
│   │   │       ├── carousel.jsx
│   │   │       ├── checkbox.jsx
│   │   │       ├── collapsible.jsx
│   │   │       ├── command.jsx
│   │   │       ├── context-menu.jsx
│   │   │       ├── dialog.jsx
│   │   │       ├── drawer.jsx
│   │   │       ├── dropdown-menu.jsx
│   │   │       ├── form.jsx
│   │   │       ├── hover-card.jsx
│   │   │       ├── input-otp.jsx
│   │   │       ├── input.jsx
│   │   │       ├── label.jsx
│   │   │       ├── menubar.jsx
│   │   │       ├── navigation-menu.jsx
│   │   │       ├── pagination.jsx
│   │   │       ├── popover.jsx
│   │   │       ├── progress.jsx
│   │   │       ├── radio-group.jsx
│   │   │       ├── resizable.jsx
│   │   │       ├── scroll-area.jsx
│   │   │       ├── select.jsx
│   │   │       ├── separator.jsx
│   │   │       ├── sheet.jsx
│   │   │       ├── skeleton.jsx
│   │   │       ├── slider.jsx
│   │   │       ├── sonner.jsx
│   │   │       ├── switch.jsx
│   │   │       ├── table.jsx
│   │   │       ├── tabs.jsx
│   │   │       ├── textarea.jsx
│   │   │       ├── toast.jsx
│   │   │       ├── toaster.jsx
│   │   │       ├── toggle-group.jsx
│   │   │       ├── toggle.jsx
│   │   │       └── tooltip.jsx
│   │   ├── constants
│   │   │   └── testIds
│   │   │       ├── auth.js
│   │   │       ├── home.js
│   │   │       └── index.js
│   │   ├── hooks
│   │   │   └── use-toast.js
│   │   ├── lib
│   │   │   └── utils.js
│   │   ├── App.css
│   │   ├── App.js
│   │   ├── index.css
│   │   └── index.js
│   ├── .gitignore
│   ├── components.json
│   ├── craco.config.js
│   ├── jsconfig.json
│   ├── package.json
│   ├── postcss.config.js
│   ├── README.md
│   ├── tailwind.config.js
│   └── yarn.lock
├── memory
│   ├── error_cache
│   │   └── errors.json
│   ├── .gitkeep
│   ├── __init__.py
│   ├── adaptateur_cognitif_rag.py
│   ├── comparaison_asymetrique_ordonnee.py
│   ├── dictionnaire_spectral.py
│   ├── directives_theorie_savard.md
│   ├── gestionnaire_erreurs.py
│   ├── memoire_conceptuelle.py
│   ├── memoire_technique.py
│   ├── PRD.md
│   ├── prompt_injector.py
│   ├── prompt_injector_enhanced.py
│   ├── test_credentials.md
│   └── theory_axioms_manager.py
├── pdf
│   └── analyse_hypothese_riemann_savard.pdf
├── src
│   └── core
│       ├── detecteur_asymetrique_ordonnee.py
│       ├── gabriel_comparaison_asymetrique.py
│       ├── gabriel_geometric_wrapper.py
│       ├── generateur_schemas_avances.py
│       ├── integrateur_memoire.py
│       ├── integrateur_memoire_patch.py
│       ├── llm_router_explicite.py
│       ├── metaphore_geometrique.py
│       └── vision_gabriel.py
├── test_reports
│   ├── pytest
│   │   └── .gitkeep
│   └── .gitkeep
├── tests
│   └── __init__.py
├── .gitconfig
├── .gitignore
├── activation_memoire.py
├── ANALYSE_GITHUB_SYNC_FEASIBILITY.md
├── ANALYSE_HOL_UNIFIEE_PROFONDE.md
├── ANALYSE_RAPPORT_SESSION_GABRIEL_DISCRIMINATION.md
├── apply_patch.ps1
├── APPLY_THEORETICAL_PATTERNS_MANUALLY.txt
├── AUTHORS
├── BADGE_QUICKSTART.md
├── BADGE_SCIENTIFIQUE_IMPLEMENTATION.md
├── BILAN_COMPLET_SESSION.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CORRECTION_DEFINITIVE_LIGNE_2605.md
├── CORRECTION_FINAL_RsP_k.thy
├── CORRECTION_GABRIEL_COMPARAISON_ASYMETRIQUE.md
├── CORRECTION_GABRIEL_COMPARAISON_RESUME.txt
├── CORRECTION_THEOREM_RsP_k.thy
├── CORRECTIONS_APPLIQUEES_CONFIRMATION.md
├── CORRECTIONS_DEFINITIVES_LIGNES_2595_2915.md
├── declaration_securite.md
├── deploy_gabriel_v6.py
├── DEPLOYMENT_STATUS.txt
├── DIAGNOSTIC_LLM_CONFLICT_OPENAI_ANTHROPIC.md
├── fichier_terminal_test_gabriel.docx
├── find_debugger.py
├── fix_corrections.py
├── fix_debugger.py
├── fix_line_2605.py
├── fix_theoretical_patterns.py
├── GABRIEL_COGNITIVE_INTEGRATION.md
├── GABRIEL_LATEX_ASSISTANT_GUIDE.md
├── gabriel_repo_mapper.py
├── GABRIEL_v7_SYSTEME_MEMOIRE.md
├── GESTION_IMAGES_3_SOLUTIONS.md
├── GUIDE_CORRECTION_THEOREM_RsP_k.md
├── LATEX_ARCHITECTURE_COMPLETE.md
├── LATEX_ASSISTANT_QUICKSTART.md
├── MEMOIRE_v7_INSTALLATION_COMPLETE.txt
├── METAPHORES_GEOMETRIQUES_GUIDE.md
├── METAPHORES_GEOMETRIQUES_QUICKSTART.md
├── PLAN_ORGANISATION.md
├── PLAN_TRIFOCAL_GUIDE_COMPLET.md
├── PLAN_TRIFOCAL_IMAGE_ACCESS.md
├── PLAN_TRIFOCAL_QUICKSTART.md
├── quick-start.bat
├── RAPPORT_FINAL_CORRECTION.txt
├── README.md
├── RELEASE_NOTES_v3.35.md
├── REPONSE_TA_QUESTION_OPENAI_BLOQUE_ANTHROPIC.md
├── RESOLUTION_ANTHROPIC_KEY_ABSENTE.md
├── RESUME_COMPLET_CORRECTION.md
├── SCHEMAS_FIGURES_VISION_GUIDE.md
├── SCHEMAS_VISION_QUICKSTART.md
├── SECURITY.md
├── security_validator.py
├── SOLUTION_DEFINITIVE_RsP_k.md
├── SOLUTION_INCOH_GABRIEL.md
├── TEST_CORRECTION_GABRIEL.py
├── test_gabriel_v6.1_gap_mixed.py
├── test_imports.py
├── test_systeme_memoire_complet.py
├── tmp_geometrie_docx.zip
├── VERIFICATION_COMPLETE_CORRECTIONS.md
├── VISION_GABRIEL_TOUS_FORMATS_CHEMIN.md
└── VISION_TOUS_FORMATS_QUICKSTART.md
```

## 2. Répartition des fichiers par type

| Type | Nombre de fichiers |
|------|--------------------|
| python | 336 |
| markdown | 229 |
| autre | 200 |
| texte | 128 |
| isabelle | 115 |
| latex | 114 |
| yaml | 18 |
| shell | 17 |
| javascript | 12 |
| json | 6 |
| html | 2 |
| css | 2 |

## 3. Fichiers les plus connectés (hub du dépôt)

| Fichier | Liens sortants résolus |
|---------|------------------------|
| `PLAN_ORGANISATION.md` | 78 |
| `agent-multiloop-Gabriel-local\ORGANISATION_GUIDE_UTILISATEUR_COMPLETE.txt` | 55 |
| `agent-multiloop-Gabriel-local\RAPPORT_ANALYSE_DEPENDANCES.md` | 50 |
| `agent-multiloop-Gabriel-local\VERIFICATION_FINALE_SYNTHESE.txt` | 45 |
| `memory\PRD.md` | 17 |
| `agent-multiloop-Gabriel-local\MOT_FIN_SESSION.txt` | 14 |
| `agent-multiloop-Gabriel-local\CHECKLIST_FINAL.md` | 12 |
| `agent-multiloop-Gabriel-local\VISUAL_SUMMARY_IMAGE_ANALYSIS.txt` | 11 |
| `BILAN_COMPLET_SESSION.md` | 11 |
| `agent-multiloop-Gabriel-local\CINEMATIC_DEPLOYMENT.md` | 10 |

## 4. Graphe des liens inter-fichiers

### `.emergent\summary.txt`
*8 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `SECURITY.md` | 128 |
| `ref_generique` | `CONTRIBUTING.md` | 128 |
| `ref_generique` | `CHANGELOG.md` | 128 |
| `ref_generique` | `declaration_securite.md` | 128 |
| `ref_generique` | `.github\workflows\build.yml` | 296 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 399 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\core\pipeline.py` | 1081 |
| `ref_generique` | `README.md` | 2084 |

### `ANALYSE_GITHUB_SYNC_FEASIBILITY.md`
*3 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 32 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\geometrie_spectre_premier.thy` | 33 |
| `ref_generique` | `agent-multiloop-Gabriel-local\memory\__init__.py` | 150 |

### `ANALYSE_HOL_UNIFIEE_PROFONDE.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\validation_hol_unifiee.thy` | 284 |

### `ANALYSE_RAPPORT_SESSION_GABRIEL_DISCRIMINATION.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 40 |

### `BADGE_QUICKSTART.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\main.py` | 11 |

### `BADGE_SCIENTIFIQUE_IMPLEMENTATION.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\main.py` | 5 |

### `BILAN_COMPLET_SESSION.md`
*11 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `CORRECTION_GABRIEL_COMPARAISON_ASYMETRIQUE.md` | 31 |
| `ref_generique` | `SOLUTION_INCOH_GABRIEL.md` | 32 |
| `ref_generique` | `RAPPORT_FINAL_CORRECTION.txt` | 33 |
| `ref_generique` | `DIAGNOSTIC_LLM_CONFLICT_OPENAI_ANTHROPIC.md` | 61 |
| `ref_generique` | `REPONSE_TA_QUESTION_OPENAI_BLOQUE_ANTHROPIC.md` | 62 |
| `ref_generique` | `agent-multiloop-Gabriel-local\docker-compose.yml` | 88 |
| `ref_generique` | `RESOLUTION_ANTHROPIC_KEY_ABSENTE.md` | 95 |
| `ref_generique` | `agent-multiloop-Gabriel-local\env.example.txt` | 108 |
| `ref_generique` | `TEST_CORRECTION_GABRIEL.py` | 141 |
| `ref_generique` | `RESUME_COMPLET_CORRECTION.md` | 150 |
| `ref_generique` | `DEPLOYMENT_STATUS.txt` | 156 |

### `CHANGELOG.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `CONTRIBUTING.md` | 226 |

### `CONTRIBUTING.md`
*8 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\requirements.txt` | 79 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\core\spectral_core.py` | 165 |
| `ref_generique` | `CHANGELOG.md` | 213 |
| `ref_generique` | `agent-multiloop-Gabriel-local\scripts\isabelle_static_check.py` | 295 |
| `ref_generique` | `agent-multiloop-Gabriel-local\tests\test_section_XI_XII_integration.py` | 295 |
| `ref_generique` | `SECURITY.md` | 350 |
| `ref_generique` | `declaration_securite.md` | 350 |
| `ref_generique` | `AUTHORS` | 358 |

### `CORRECTIONS_APPLIQUEES_CONFIRMATION.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 2 |

### `CORRECTIONS_DEFINITIVES_LIGNES_2595_2915.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 2 |

### `CORRECTION_GABRIEL_COMPARAISON_RESUME.txt`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` | 148 |

### `DIAGNOSTIC_LLM_CONFLICT_OPENAI_ANTHROPIC.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\config.yaml` | 16 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` | 346 |

### `GABRIEL_COGNITIVE_INTEGRATION.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 7 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\validation_hol_unifiee.thy` | 202 |

### `GABRIEL_v7_SYSTEME_MEMOIRE.md`
*5 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `memory\memoire_conceptuelle.py` | 70 |
| `ref_generique` | `memory\memoire_technique.py` | 74 |
| `ref_generique` | `memory\gestionnaire_erreurs.py` | 78 |
| `ref_generique` | `memory\error_cache\errors.json` | 83 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` | 86 |

### `GESTION_IMAGES_3_SOLUTIONS.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\docker-compose.yml` | 12 |
| `ref_generique` | `src\core\vision_gabriel.py` | 318 |

### `GUIDE_CORRECTION_THEOREM_RsP_k.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 2 |

### `MEMOIRE_v7_INSTALLATION_COMPLETE.txt`
*6 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `memory\memoire_conceptuelle.py` | 8 |
| `ref_generique` | `memory\memoire_technique.py` | 9 |
| `ref_generique` | `memory\gestionnaire_erreurs.py` | 10 |
| `ref_generique` | `agent-multiloop-Gabriel-local\memory\__init__.py` | 12 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` | 15 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\core\llm_manager.py` | 16 |

### `METAPHORES_GEOMETRIQUES_GUIDE.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` | 303 |

### `METAPHORES_GEOMETRIQUES_QUICKSTART.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` | 15 |

### `PLAN_ORGANISATION.md`
*78 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\GO_QUICK_START.md` | 15 |
| `ref_generique` | `agent-multiloop-Gabriel-local\REPONSE_RAPIDE_RECONSTRUCTION.md` | 16 |
| `ref_generique` | `agent-multiloop-Gabriel-local\QUICK_START_5_MINUTES.md` | 17 |
| `ref_generique` | `agent-multiloop-Gabriel-local\QUICK_START_IMAGE_ANALYSIS.md` | 18 |
| `ref_generique` | `README.md` | 19 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md` | 22 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_IMAGE_ANALYSIS_COMPLETE_GUIDE.md` | 23 |
| `ref_generique` | `agent-multiloop-Gabriel-local\IMAGE_ANALYSIS_ANSWER_DIRECT.md` | 24 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GUIDE_ANALYSE_AVEC_CRITERES.md` | 25 |
| `ref_generique` | `agent-multiloop-Gabriel-local\COMMANDES_PRATIQUES_ANALYSE.md` | 26 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GUIDE_RECONSTRUCTION_REDEMARRAGE.md` | 30 |
| `ref_generique` | `agent-multiloop-Gabriel-local\FINAL_RECONSTRUCTION_SUMMARY.txt` | 31 |
| `ref_generique` | `agent-multiloop-Gabriel-local\VALIDATION_HOL_UNIFIEE_ANALYSIS.md` | 35 |
| `ref_generique` | `agent-multiloop-Gabriel-local\VALIDATION_HOL_INTEGRATION_COMPLETE.md` | 36 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_VISION_QUICK_START.md` | 40 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` | 41 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_VISION_VERIFICATION_COMPLETE.md` | 42 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_COMPLETE_VISION_INTEGRATION.md` | 43 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CINEMATIC_DEPLOYMENT.md` | 47 |
| `ref_generique` | `agent-multiloop-Gabriel-local\DEPLOYMENT_CHECKLIST_v4.0.md` | 48 |
| `ref_generique` | `agent-multiloop-Gabriel-local\DEPLOYMENT_SUMMARY.md` | 49 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v5.4_WORKING_SOLUTION.md` | 50 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CONFIG_ENV_GUIDE.md` | 54 |
| `ref_generique` | `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` | 55 |
| `ref_generique` | `agent-multiloop-Gabriel-local\UTF8_ENCODING_FIX.md` | 56 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GUIDE_JEDIT_GABRIEL.md` | 60 |
| `ref_generique` | `agent-multiloop-Gabriel-local\POWERSHELL_ISE_GUIDE.md` | 61 |
| `ref_generique` | `agent-multiloop-Gabriel-local\JEDIT_QUICK_REFERENCE.md` | 62 |
| `ref_generique` | `agent-multiloop-Gabriel-local\SHORTCUTS_AND_TIPS.md` | 63 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PYTEST_CHECKLIST.md` | 67 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PYTEST_EXECUTION_GUIDE.md` | 68 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PYTEST_INDEX.md` | 69 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PYTEST_LIST_COMPLETE.md` | 70 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PYTEST_SUMMARY.md` | 71 |
| `ref_generique` | `agent-multiloop-Gabriel-local\COMMANDS_COMPLETE_REFERENCE.md` | 75 |
| `ref_generique` | `agent-multiloop-Gabriel-local\QUICK_REFERENCE.md` | 76 |
| `ref_generique` | `agent-multiloop-Gabriel-local\guide_utilisateur\01_DEMARRAGE_RAPIDE\INDEX.md` | 77 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CORRECTION_RSA_v2.2.md` | 83 |
| `ref_generique` | `agent-multiloop-Gabriel-local\SYNTHESE_RSA_v2.2.md` | 84 |
| `ref_generique` | `agent-multiloop-Gabriel-local\SYNTHESE_ULTIME_v2.1.md` | 85 |
| `ref_generique` | `agent-multiloop-Gabriel-local\HOL_ISABELLE_FIX.md` | 86 |
| `ref_generique` | `agent-multiloop-Gabriel-local\HOL4_SYSTEMATIC_PROOFS.md` | 87 |
| `ref_generique` | `agent-multiloop-Gabriel-local\BUG_FIX_URGENT_HOL.md` | 88 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v2.1_RELEASE_NOTES.md` | 92 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v2.2_RSA_CAPABILITY.md` | 93 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v3.0_MULTILOOP_VALIDATION.md` | 94 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v4.0_THEORY_MEMORY.md` | 95 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v5.0_LLM_ROUTING.md` | 96 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v5.1_SAFE_BUDGET.md` | 97 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v5.2_DEPLOYMENT_SUMMARY.md` | 98 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v5.2_HOL_FORMAL.md` | 99 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v5_UPDATE_GUIDE.md` | 100 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` | 102 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md` | 103 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CINEMATIC_INTEGRATION_GUIDE.md` | 107 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CINEMATIC_MODE_SUMMARY.md` | 108 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_DOMAIN_SYSTEM_INTEGRATION_GUIDE.md` | 109 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_PARAMETRIC_VALIDATION_GUIDE.md` | 110 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_PRODUCTION_VALIDATION_GUIDE.md` | 111 |
| `ref_generique` | `agent-multiloop-Gabriel-local\INTEGRATION_UNIVERSESTAUCARRE.md` | 112 |
| `ref_generique` | `agent-multiloop-Gabriel-local\MIGRATION_VALIDATION_SYSTEMS.md` | 113 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PATCH_THEORETICAL_RECOGNITION.md` | 114 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_PERFORMANCE_OPTIMIZATION.md` | 118 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_PORT_FIX_v5.3.md` | 119 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_FINAL_v5_SOCKET_CLEANUP.md` | 120 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PORT_CLEANUP_IMPLEMENTATION.md` | 121 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_DEBUGGER_PAUSE_STATUS.md` | 125 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CLAUDE_BUDGET_GUIDE.md` | 126 |
| `ref_generique` | `agent-multiloop-Gabriel-local\OPTIMIZATION_SUMMARY.md` | 127 |
| `ref_generique` | `agent-multiloop-Gabriel-local\MULTIFORMAT_TEMPLATES_GUIDE.md` | 129 |
| `ref_generique` | `agent-multiloop-Gabriel-local\FINAL_300_TEMPLATES_SUMMARY.md` | 130 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PROJECTS_TEMPLATES_GUIDE.md` | 131 |
| `ref_generique` | `agent-multiloop-Gabriel-local\TEMPLATES_SUMMARY.md` | 132 |
| `ref_generique` | `agent-multiloop-Gabriel-local\FILES_v5.0.md` | 133 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CHECKLIST_FINAL.md` | 134 |
| `ref_generique` | `agent-multiloop-Gabriel-local\TODO_ANALYSE.md` | 135 |
| `ref_generique` | `CHANGELOG.md` | 136 |
| `ref_generique` | `agent-multiloop-Gabriel-local\REPONSE_OUI_PREUVES_HOL4_SYSTEMATIQUES.md` | 137 |

### `PLAN_TRIFOCAL_GUIDE_COMPLET.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 253 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\ui\cli.py` | 253 |

### `PLAN_TRIFOCAL_IMAGE_ACCESS.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 57 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\ui\cli.py` | 57 |

### `RAPPORT_FINAL_CORRECTION.txt`
*5 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `CORRECTION_GABRIEL_COMPARAISON_ASYMETRIQUE.md` | 56 |
| `ref_generique` | `SOLUTION_INCOH_GABRIEL.md` | 57 |
| `ref_generique` | `CORRECTION_GABRIEL_COMPARAISON_RESUME.txt` | 58 |
| `ref_generique` | `src\core\integrateur_memoire_patch.py` | 146 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` | 177 |

### `REPONSE_TA_QUESTION_OPENAI_BLOQUE_ANTHROPIC.md`
*3 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `DIAGNOSTIC_LLM_CONFLICT_OPENAI_ANTHROPIC.md` | 241 |
| `ref_generique` | `src\core\llm_router_explicite.py` | 246 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` | 247 |

### `RESOLUTION_ANTHROPIC_KEY_ABSENTE.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\docker-compose.yml` | 6 |
| `ref_generique` | `agent-multiloop-Gabriel-local\config.yaml` | 33 |

### `RESUME_COMPLET_CORRECTION.md`
*3 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `src\core\detecteur_asymetrique_ordonnee.py` | 32 |
| `ref_generique` | `memory\comparaison_asymetrique_ordonnee.py` | 38 |
| `ref_generique` | `src\core\gabriel_comparaison_asymetrique.py` | 44 |

### `SCHEMAS_FIGURES_VISION_GUIDE.md`
*3 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `src\core\generateur_schemas_avances.py` | 312 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` | 313 |
| `ref_generique` | `src\core\vision_gabriel.py` | 317 |

### `SCHEMAS_VISION_QUICKSTART.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `src\core\generateur_schemas_avances.py` | 18 |
| `ref_generique` | `src\core\vision_gabriel.py` | 27 |

### `SECURITY.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `declaration_securite.md` | 3 |

### `SOLUTION_DEFINITIVE_RsP_k.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 206 |

### `SOLUTION_INCOH_GABRIEL.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `memory\comparaison_asymetrique_ordonnee.py` | 26 |

### `TEST_CORRECTION_GABRIEL.py`
*3 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `src\core\detecteur_asymetrique_ordonnee.py` | 19 |
| `import_module` | `src\core\gabriel_comparaison_asymetrique.py` | 21 |
| `import_module` | `memory\comparaison_asymetrique_ordonnee.py` | 22 |

### `VERIFICATION_COMPLETE_CORRECTIONS.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 4 |

### `VISION_GABRIEL_TOUS_FORMATS_CHEMIN.md`
*3 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `src\core\vision_gabriel.py` | 4 |
| `ref_generique` | `.` | 116 |
| `ref_generique` | `agent-multiloop-Gabriel-local\docker-compose.yml` | 157 |

### `VISION_TOUS_FORMATS_QUICKSTART.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `src\core\vision_gabriel.py` | 4 |

### `activation_memoire.py`
*7 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `Path()` | `memory` | 18 |
| `Path()` | `agent-multiloop-Gabriel-local\src\core\llm_manager.py` | 44 |
| `Path()` | `src\core\integrateur_memoire.py` | 59 |
| `chemin_litteral` | `memory\memoire_conceptuelle.py` | 20 |
| `chemin_litteral` | `memory\memoire_technique.py` | 21 |
| `chemin_litteral` | `memory\gestionnaire_erreurs.py` | 22 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\memory\__init__.py` | 24 |

### `agent-multiloop-Gabriel-local\00_START_HERE_IMAGE_ANALYSIS.md`
*3 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\gabriel_vision_integration.py` | 25 |
| `ref_generique` | `agent-multiloop-Gabriel-local\COMPLETE_INTEGRATION_INSTRUCTIONS.md` | 26 |
| `ref_generique` | `agent-multiloop-Gabriel-local\INTEGRATION_PATCH_IMAGE_ANALYSIS.md` | 50 |

### `agent-multiloop-Gabriel-local\CHANGELOG.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 102 |
| `ref_generique` | `agent-multiloop-Gabriel-local\docker-compose.yml` | 140 |

### `agent-multiloop-Gabriel-local\CHECKLIST_FINAL.md`
*12 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\mathematical_engine.py` | 111 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\hol_lean_interface.py` | 112 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\pdf_rag_processor.py` | 113 |
| `ref_generique` | `agent-multiloop-Gabriel-local\memory\__init__.py` | 114 |
| `ref_generique` | `agent-multiloop-Gabriel-local\gabriel_mathematical.py` | 127 |
| `ref_generique` | `agent-multiloop-Gabriel-local\integration_mathematical.py` | 128 |
| `ref_generique` | `agent-multiloop-Gabriel-local\requirements.txt` | 130 |
| `ref_generique` | `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` | 133 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CHECKLIST_FINAL.md` | 134 |
| `ref_generique` | `agent-multiloop-Gabriel-local\main.py` | 136 |
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 137 |
| `ref_generique` | `backend\server.py` | 141 |

### `agent-multiloop-Gabriel-local\CINEMATIC_DEPLOYMENT.md`
*10 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\CINEMATIC_INTEGRATION_GUIDE.md` | 13 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CINEMATIC_MODE_SUMMARY.md` | 14 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CINEMATIC_EXAMPLES.py` | 15 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CINEMATIC_DEPLOYMENT.md` | 16 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\ui\cinematic_display.py` | 31 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\ui\cinematic_orchestrator.py` | 32 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\ui\complexity_analyzer.py` | 33 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\ui\cli.py` | 147 |
| `ref_generique` | `agent-multiloop-Gabriel-local\docker-compose.yml` | 171 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\core\pipeline.py` | 202 |

### `agent-multiloop-Gabriel-local\CINEMATIC_EXAMPLES.py`
*3 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `agent-multiloop-Gabriel-local\src\ui\complexity_analyzer.py` | 18 |
| `import_module` | `agent-multiloop-Gabriel-local\src\ui\cinematic_display.py` | 19 |
| `import_module` | `agent-multiloop-Gabriel-local\src\ui\cinematic_orchestrator.py` | 20 |

### `agent-multiloop-Gabriel-local\CINEMATIC_INTEGRATION_GUIDE.md`
*3 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 26 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\ui\complexity_analyzer.py` | 164 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\ui\ask_gabriel.py` | 219 |

### `agent-multiloop-Gabriel-local\CINEMATIC_MODE_SUMMARY.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\ui\complexity_analyzer.py` | 178 |

### `agent-multiloop-Gabriel-local\CLAUDE_BUDGET_GUIDE.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\llm_router.py` | 39 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\cost_manager.py` | 49 |

### `agent-multiloop-Gabriel-local\COMMANDES_PRATIQUES_ANALYSE.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 168 |

### `agent-multiloop-Gabriel-local\COMPLETE_INTEGRATION_INSTRUCTIONS.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\ui\cli.py` | 273 |

### `agent-multiloop-Gabriel-local\CORRECTION_RSA_v2.2.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\test_rsa_capability.py` | 129 |

### `agent-multiloop-Gabriel-local\DEPLOYMENT_CHECKLIST_v4.0.md`
*10 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\docker-compose.yml` | 6 |
| `ref_generique` | `agent-multiloop-Gabriel-local\requirements.txt` | 7 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\adapters\gabriel_isabelle_bridge.py` | 65 |
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 73 |
| `ref_generique` | `agent-multiloop-Gabriel-local\scripts\isabelle-integration.sh` | 81 |
| `ref_generique` | `agent-multiloop-Gabriel-local\INTEGRATION_UNIVERSESTAUCARRE.md` | 106 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GUIDE_JEDIT_GABRIEL.md` | 107 |
| `ref_generique` | `agent-multiloop-Gabriel-local\JEDIT_QUICK_REFERENCE.md` | 108 |
| `ref_generique` | `agent-multiloop-Gabriel-local\quick-start.sh` | 109 |
| `ref_generique` | `agent-multiloop-Gabriel-local\test-integration.sh` | 110 |

### `agent-multiloop-Gabriel-local\DEPLOYMENT_READY.txt`
*6 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\COMPLETE_INTEGRATION_INSTRUCTIONS.md` | 24 |
| `ref_generique` | `agent-multiloop-Gabriel-local\apply_image_analysis_patch.py` | 28 |
| `ref_generique` | `agent-multiloop-Gabriel-local\deploy_image_analysis.py` | 32 |
| `ref_generique` | `agent-multiloop-Gabriel-local\00_START_HERE_IMAGE_ANALYSIS.md` | 38 |
| `ref_generique` | `agent-multiloop-Gabriel-local\INTEGRATION_PATCH_IMAGE_ANALYSIS.md` | 39 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\ui\cli.py` | 216 |

### `agent-multiloop-Gabriel-local\DEPLOYMENT_SUMMARY.md`
*4 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\requirements.txt` | 65 |
| `ref_generique` | `agent-multiloop-Gabriel-local\gabriel_mathematical.py` | 78 |
| `ref_generique` | `agent-multiloop-Gabriel-local\quick_verification.py` | 232 |
| `ref_generique` | `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` | 299 |

### `agent-multiloop-Gabriel-local\EXEMPLE_GABRIEL_v2.1.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `agent-multiloop-Gabriel-local\gabriel_mathematical.py` | 5 |

### `agent-multiloop-Gabriel-local\FINAL_300_TEMPLATES_SUMMARY.md`
*8 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_01.thy` | 8 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_02.thy` | 9 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_100.thy` | 11 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_01.txt` | 20 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_02.txt` | 21 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_100.txt` | 23 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_42.thy` | 83 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_42.txt` | 86 |

### `agent-multiloop-Gabriel-local\GABRIEL_COMPLETE_VISION_INTEGRATION.md`
*7 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 4 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\ui\ask_gabriel.py` | 4 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\image_access_manager.py` | 196 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\vision_module.py` | 197 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\advanced_vision_module.py` | 198 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\gabriel_vision_integration.py` | 199 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\complete_vision_system.py` | 200 |

### `agent-multiloop-Gabriel-local\GABRIEL_DEBUGGER_PAUSE_STATUS.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 15 |

### `agent-multiloop-Gabriel-local\GABRIEL_DOMAIN_SYSTEM_INTEGRATION_GUIDE.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\multiloop\slow_motion_debugger.py` | 176 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\multiloop\domain_gate.py` | 316 |

### `agent-multiloop-Gabriel-local\GABRIEL_FINAL_v5_SOCKET_CLEANUP.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\socket_cleanup.py` | 75 |
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 76 |

### `agent-multiloop-Gabriel-local\GABRIEL_IMAGE_ANALYSIS_COMPLETE_GUIDE.md`
*8 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 185 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\complete_vision_system.py` | 357 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\production_validation_system.py` | 358 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\image_access_manager.py` | 359 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\vision_module.py` | 360 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\advanced_vision_module.py` | 361 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\gabriel_image_interface.py` | 362 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\ui\cli.py` | 364 |

### `agent-multiloop-Gabriel-local\GABRIEL_PERFORMANCE_OPTIMIZATION.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 77 |

### `agent-multiloop-Gabriel-local\GABRIEL_PORT_FIX_v5.3.md`
*4 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\gabriel_control.py` | 50 |
| `ref_generique` | `agent-multiloop-Gabriel-local\docker-compose.yml` | 195 |
| `ref_generique` | `agent-multiloop-Gabriel-local\gabriel_launcher.py` | 196 |
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 196 |

### `agent-multiloop-Gabriel-local\GABRIEL_VISION_QUICK_START.md`
*9 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\image_access_manager.py` | 7 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\vision_module.py` | 8 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\advanced_vision_module.py` | 9 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\gabriel_vision_integration.py` | 10 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\complete_vision_system.py` | 11 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` | 14 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_COMPLETE_VISION_INTEGRATION.md` | 15 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_VISION_VERIFICATION_COMPLETE.md` | 16 |
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 40 |

### `agent-multiloop-Gabriel-local\GABRIEL_VISION_VERIFICATION_COMPLETE.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 234 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_COMPLETE_VISION_INTEGRATION.md` | 234 |

### `agent-multiloop-Gabriel-local\GABRIEL_v2.1_RELEASE_NOTES.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\gabriel_mathematical.py` | 210 |
| `ref_generique` | `agent-multiloop-Gabriel-local\HOL4_SYSTEMATIC_PROOFS.md` | 212 |

### `agent-multiloop-Gabriel-local\GABRIEL_v3.0_MULTILOOP_VALIDATION.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\gabriel_mathematical.py` | 339 |

### `agent-multiloop-Gabriel-local\GABRIEL_v4.0_THEORY_MEMORY.md`
*4 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `memory\directives_theorie_savard.md` | 29 |
| `ref_generique` | `memory\theory_axioms_manager.py` | 30 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\prompt_injector.py` | 31 |
| `ref_generique` | `agent-multiloop-Gabriel-local\gabriel_mathematical.py` | 232 |

### `agent-multiloop-Gabriel-local\GABRIEL_v5.0_FINAL_SUMMARY.txt`
*4 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\socket_cleanup.py` | 66 |
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 87 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_FINAL_v5_SOCKET_CLEANUP.md` | 243 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v5_UPDATE_GUIDE.md` | 244 |

### `agent-multiloop-Gabriel-local\GABRIEL_v5.4_WORKING_SOLUTION.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 26 |
| `ref_generique` | `agent-multiloop-Gabriel-local\gabriel_launcher.py` | 82 |

### `agent-multiloop-Gabriel-local\GUIDE_ANALYSE_AVEC_CRITERES.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 398 |

### `agent-multiloop-Gabriel-local\GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 401 |

### `agent-multiloop-Gabriel-local\GUIDE_JEDIT_GABRIEL.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\docker-compose.yml` | 45 |

### `agent-multiloop-Gabriel-local\GUIDE_RECONSTRUCTION_REDEMARRAGE.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 56 |
| `ref_generique` | `agent-multiloop-Gabriel-local\requirements.txt` | 182 |

### `agent-multiloop-Gabriel-local\HOL_ISABELLE_FIX.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\spectral\hol_script_generator.py` | 43 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\adapters\hol_integration.py` | 56 |

### `agent-multiloop-Gabriel-local\INDEX.md`
*7 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\gabriel_launcher.py` | 85 |
| `ref_generique` | `agent-multiloop-Gabriel-local\START_HERE.txt` | 136 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` | 138 |
| `ref_generique` | `agent-multiloop-Gabriel-local\QUICK_REFERENCE.md` | 207 |
| `ref_generique` | `agent-multiloop-Gabriel-local\POWERSHELL_ISE_GUIDE.md` | 208 |
| `ref_generique` | `agent-multiloop-Gabriel-local\SHORTCUTS_AND_TIPS.md` | 209 |
| `ref_generique` | `agent-multiloop-Gabriel-local\docker-compose.yml` | 210 |

### `agent-multiloop-Gabriel-local\INTEGRATION_PATCH_IMAGE_ANALYSIS.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\ui\cli.py` | 14 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\gabriel_vision_integration.py` | 161 |

### `agent-multiloop-Gabriel-local\INTEGRATION_UNIVERSESTAUCARRE.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\docker-compose.yml` | 114 |

### `agent-multiloop-Gabriel-local\JEDIT_QUICK_REFERENCE.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 187 |

### `agent-multiloop-Gabriel-local\MIGRATION_VALIDATION_SYSTEMS.md`
*3 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\parametric_validation_module.py` | 266 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\complete_validation_integration.py` | 267 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\production_validation_system.py` | 270 |

### `agent-multiloop-Gabriel-local\MOT_FIN_SESSION.txt`
*14 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\gabriel_image_interface.py` | 42 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\image_discovery_system.py` | 43 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\advanced_analysis_criteria.py` | 44 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\validation_hol_knowledge.py` | 54 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GO_QUICK_START.md` | 152 |
| `ref_generique` | `agent-multiloop-Gabriel-local\QUICK_START_5_MINUTES.md` | 153 |
| `ref_generique` | `agent-multiloop-Gabriel-local\REPONSE_RAPIDE_RECONSTRUCTION.md` | 154 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md` | 157 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_IMAGE_ANALYSIS_COMPLETE_GUIDE.md` | 158 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GUIDE_ANALYSE_AVEC_CRITERES.md` | 159 |
| `ref_generique` | `agent-multiloop-Gabriel-local\COMMANDES_PRATIQUES_ANALYSE.md` | 160 |
| `ref_generique` | `agent-multiloop-Gabriel-local\RAPPORT_ANALYSE_DEPENDANCES.md` | 163 |
| `ref_generique` | `agent-multiloop-Gabriel-local\VERIFICATION_FINALE_SYNTHESE.txt` | 164 |
| `ref_generique` | `PLAN_ORGANISATION.md` | 165 |

### `agent-multiloop-Gabriel-local\MULTIFORMAT_TEMPLATES_GUIDE.md`
*7 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_01.thy` | 9 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_02.thy` | 10 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_100.thy` | 12 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_01.txt` | 15 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_02.txt` | 16 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_100.txt` | 18 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_42.thy` | 340 |

### `agent-multiloop-Gabriel-local\OPTIMIZATION_SUMMARY.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\config_optimized.yaml` | 66 |
| `ref_generique` | `agent-multiloop-Gabriel-local\apply_optimization.py` | 67 |

### `agent-multiloop-Gabriel-local\ORGANISATION_GUIDE_UTILISATEUR_COMPLETE.txt`
*55 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\README.md` | 22 |
| `ref_generique` | `agent-multiloop-Gabriel-local\INDEX.md` | 24 |
| `ref_generique` | `agent-multiloop-Gabriel-local\QUICK_START_5_MINUTES.md` | 85 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GO_QUICK_START.md` | 86 |
| `ref_generique` | `agent-multiloop-Gabriel-local\QUICK_REFERENCE.md` | 87 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md` | 91 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CINEMATIC_MODE_SUMMARY.md` | 92 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CINEMATIC_INTEGRATION_GUIDE.md` | 93 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CINEMATIC_EXAMPLES.py` | 94 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CINEMATIC_DEPLOYMENT.md` | 95 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md` | 99 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GUIDE_ANALYSE_AVEC_CRITERES.md` | 100 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_IMAGE_ANALYSIS_COMPLETE_GUIDE.md` | 101 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_VISION_QUICK_START.md` | 102 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_VISION_VERIFICATION_COMPLETE.md` | 103 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` | 104 |
| `ref_generique` | `agent-multiloop-Gabriel-local\QUICK_START_IMAGE_ANALYSIS.md` | 105 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` | 109 |
| `ref_generique` | `agent-multiloop-Gabriel-local\DEPLOYMENT_SUMMARY.md` | 110 |
| `ref_generique` | `agent-multiloop-Gabriel-local\DEPLOYMENT_CHECKLIST_v4.0.md` | 111 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_PORT_FIX_v5.3.md` | 112 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PORT_CLEANUP_IMPLEMENTATION.md` | 113 |
| `ref_generique` | `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` | 117 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v4.0_THEORY_MEMORY.md` | 118 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v5.0_LLM_ROUTING.md` | 119 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_PARAMETRIC_VALIDATION_GUIDE.md` | 120 |
| `ref_generique` | `agent-multiloop-Gabriel-local\HOL_ISABELLE_FIX.md` | 121 |
| `ref_generique` | `agent-multiloop-Gabriel-local\HOL4_SYSTEMATIC_PROOFS.md` | 122 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v5.2_HOL_FORMAL.md` | 123 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GUIDE_RECONSTRUCTION_REDEMARRAGE.md` | 127 |
| `ref_generique` | `agent-multiloop-Gabriel-local\REPONSE_RAPIDE_RECONSTRUCTION.md` | 128 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_COMPLETE_VISION_INTEGRATION.md` | 129 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PYTEST_SUMMARY.md` | 133 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PYTEST_EXECUTION_GUIDE.md` | 134 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PYTEST_CHECKLIST.md` | 135 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PYTEST_LIST_COMPLETE.md` | 136 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PYTEST_INDEX.md` | 137 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_PRODUCTION_VALIDATION_GUIDE.md` | 138 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_VALIDATION_EXAMPLES.md` | 139 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CONFIG_ENV_GUIDE.md` | 143 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CLAUDE_BUDGET_GUIDE.md` | 144 |
| `ref_generique` | `agent-multiloop-Gabriel-local\POWERSHELL_ISE_GUIDE.md` | 145 |
| `ref_generique` | `agent-multiloop-Gabriel-local\JEDIT_QUICK_REFERENCE.md` | 146 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GUIDE_JEDIT_GABRIEL.md` | 147 |
| `ref_generique` | `agent-multiloop-Gabriel-local\COMMANDS_COMPLETE_REFERENCE.md` | 152 |
| `ref_generique` | `agent-multiloop-Gabriel-local\COMMANDES_PRATIQUES_ANALYSE.md` | 153 |
| `ref_generique` | `agent-multiloop-Gabriel-local\SHORTCUTS_AND_TIPS.md` | 154 |
| `ref_generique` | `agent-multiloop-Gabriel-local\RAPPORT_ETAPE1_ANALYSE_README.md` | 159 |
| `ref_generique` | `agent-multiloop-Gabriel-local\RAPPORT_ETAPE2_ANALYSE_ARCHITECTURE.md` | 160 |
| `ref_generique` | `agent-multiloop-Gabriel-local\RAPPORT_MAINTENANCE_ETAPE3.md` | 161 |
| `ref_generique` | `agent-multiloop-Gabriel-local\RAPPORT_ANALYSE_DEPENDANCES.md` | 162 |
| `ref_generique` | `agent-multiloop-Gabriel-local\RELEASE_NOTES_v2.1.md` | 166 |
| `ref_generique` | `agent-multiloop-Gabriel-local\ETAPE5_AMELIORATIONS_PRIORITAIRES.md` | 167 |
| `ref_generique` | `agent-multiloop-Gabriel-local\RELEASE_v2.1_COMPLETE.txt` | 168 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CHANGELOG.md` | 169 |

### `agent-multiloop-Gabriel-local\PORT_CLEANUP_IMPLEMENTATION.md`
*4 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\gabriel_launcher.py` | 40 |
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 40 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\tex` | 82 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\tex\README_pdf.md` | 118 |

### `agent-multiloop-Gabriel-local\PROJECTS_TEMPLATES_GUIDE.md`
*3 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_01.thy` | 105 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_02.thy` | 106 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_100.thy` | 108 |

### `agent-multiloop-Gabriel-local\PYTEST_CHECKLIST.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\spectral\prime_table.py` | 130 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\spectral\gap_solver_corrected.py` | 131 |

### `agent-multiloop-Gabriel-local\QUICK_REFERENCE.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\docker-compose.yml` | 151 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_FINAL_SOLUTION.txt` | 152 |

### `agent-multiloop-Gabriel-local\QUICK_START_5_MINUTES.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 66 |

### `agent-multiloop-Gabriel-local\QUICK_START_IMAGE_ANALYSIS.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\validation_hol_unifiee.thy` | 273 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_IMAGE_ANALYSIS_COMPLETE_GUIDE.md` | 334 |

### `agent-multiloop-Gabriel-local\RAPPORT_ANALYSE_DEPENDANCES.md`
*50 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\FINAL_RECONSTRUCTION_SUMMARY.txt` | 50 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GUIDE_RECONSTRUCTION_REDEMARRAGE.md` | 51 |
| `ref_generique` | `agent-multiloop-Gabriel-local\REPONSE_RAPIDE_RECONSTRUCTION.md` | 52 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GO_QUICK_START.md` | 53 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GUIDE_ANALYSE_AVEC_CRITERES.md` | 54 |
| `ref_generique` | `agent-multiloop-Gabriel-local\COMMANDES_PRATIQUES_ANALYSE.md` | 55 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md` | 56 |
| `ref_generique` | `agent-multiloop-Gabriel-local\IMAGE_ANALYSIS_ANSWER_DIRECT.md` | 57 |
| `ref_generique` | `agent-multiloop-Gabriel-local\QUICK_START_IMAGE_ANALYSIS.md` | 58 |
| `ref_generique` | `agent-multiloop-Gabriel-local\QUICK_START_5_MINUTES.md` | 59 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_IMAGE_ANALYSIS_COMPLETE_GUIDE.md` | 60 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_VISION_QUICK_START.md` | 61 |
| `ref_generique` | `PLAN_ORGANISATION.md` | 81 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` | 104 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_VISION_VERIFICATION_COMPLETE.md` | 105 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_COMPLETE_VISION_INTEGRATION.md` | 106 |
| `ref_generique` | `agent-multiloop-Gabriel-local\VALIDATION_HOL_UNIFIEE_ANALYSIS.md` | 112 |
| `ref_generique` | `agent-multiloop-Gabriel-local\VALIDATION_HOL_INTEGRATION_COMPLETE.md` | 113 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CONFIG_ENV_GUIDE.md` | 119 |
| `ref_generique` | `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` | 120 |
| `ref_generique` | `agent-multiloop-Gabriel-local\UTF8_ENCODING_FIX.md` | 121 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PYTEST_CHECKLIST.md` | 127 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PYTEST_EXECUTION_GUIDE.md` | 128 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PYTEST_INDEX.md` | 129 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PYTEST_LIST_COMPLETE.md` | 130 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PYTEST_SUMMARY.md` | 131 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v2.1_RELEASE_NOTES.md` | 137 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v2.2_RSA_CAPABILITY.md` | 138 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v3.0_MULTILOOP_VALIDATION.md` | 139 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v4.0_THEORY_MEMORY.md` | 140 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v5.0_LLM_ROUTING.md` | 141 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v5.1_SAFE_BUDGET.md` | 142 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v5.2_DEPLOYMENT_SUMMARY.md` | 143 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v5.2_HOL_FORMAL.md` | 144 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v5_UPDATE_GUIDE.md` | 145 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` | 147 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md` | 148 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CHANGELOG.md` | 154 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CHECKLIST_FINAL.md` | 155 |
| `ref_generique` | `agent-multiloop-Gabriel-local\TODO_ANALYSE.md` | 156 |
| `ref_generique` | `agent-multiloop-Gabriel-local\FILES_v5.0.md` | 157 |
| `ref_generique` | `agent-multiloop-Gabriel-local\FINAL_300_TEMPLATES_SUMMARY.md` | 158 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CLAUDE_BUDGET_GUIDE.md` | 159 |
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 170 |
| `ref_generique` | `agent-multiloop-Gabriel-local\main.py` | 171 |
| `ref_generique` | `agent-multiloop-Gabriel-local\requirements.txt` | 183 |
| `ref_generique` | `agent-multiloop-Gabriel-local\apply_optimization.py` | 189 |
| `ref_generique` | `agent-multiloop-Gabriel-local\cognitive_pipeline_hol_unified.py` | 190 |
| `ref_generique` | `agent-multiloop-Gabriel-local\INTEGRATION_MANUELLE.py` | 191 |
| `ref_generique` | `agent-multiloop-Gabriel-local\EXEMPLE_GABRIEL_v2.1.py` | 192 |

### `agent-multiloop-Gabriel-local\RAPPORT_ETAPE1_ANALYSE_README.md`
*3 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\README.md` | 8 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` | 9 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md` | 12 |

### `agent-multiloop-Gabriel-local\RAPPORT_ETAPE2_ANALYSE_ARCHITECTURE.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\README.md` | 371 |

### `agent-multiloop-Gabriel-local\RAPPORT_MAINTENANCE_ETAPE3.md`
*3 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\README.md` | 76 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` | 78 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md` | 80 |

### `agent-multiloop-Gabriel-local\README.md`
*5 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\spectral\prime_table.py` | 191 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README.md` | 207 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` | 208 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md` | 209 |
| `ref_generique` | `agent-multiloop-Gabriel-local\docker-compose.yml` | 211 |

### `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md`
*4 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\CINEMATIC_INTEGRATION_GUIDE.md` | 318 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CINEMATIC_MODE_SUMMARY.md` | 319 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md` | 320 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GUIDE_ANALYSE_AVEC_CRITERES.md` | 321 |

### `agent-multiloop-Gabriel-local\RELEASE_NOTES_v2.1.md`
*4 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md` | 38 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README.md` | 39 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` | 133 |
| `ref_generique` | `agent-multiloop-Gabriel-local\RAPPORT_ETAPE2_ANALYSE_ARCHITECTURE.md` | 141 |

### `agent-multiloop-Gabriel-local\RELEASE_v2.1_COMPLETE.txt`
*10 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\RAPPORT_ETAPE1_ANALYSE_README.md` | 20 |
| `ref_generique` | `agent-multiloop-Gabriel-local\RAPPORT_ETAPE2_ANALYSE_ARCHITECTURE.md` | 26 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md` | 31 |
| `ref_generique` | `agent-multiloop-Gabriel-local\RAPPORT_MAINTENANCE_ETAPE3.md` | 33 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README.md` | 36 |
| `ref_generique` | `agent-multiloop-Gabriel-local\RELEASE_NOTES_v2.1.md` | 37 |
| `ref_generique` | `agent-multiloop-Gabriel-local\ETAPE5_AMELIORATIONS_PRIORITAIRES.md` | 46 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\image_discovery_system.py` | 80 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\advanced_analysis_criteria.py` | 87 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` | 109 |

### `agent-multiloop-Gabriel-local\RESUME_SESSION_COMPLETE.md`
*4 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\gabriel_image_interface.py` | 91 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\image_discovery_system.py` | 92 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\advanced_analysis_criteria.py` | 93 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\validation_hol_knowledge.py` | 95 |

### `agent-multiloop-Gabriel-local\SECURITY_FIXES_SUMMARY.md`
*6 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\socket_cleanup.py` | 64 |
| `ref_generique` | `agent-multiloop-Gabriel-local\port_cleanup.py` | 78 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\engines\abstraction\abstraction_layer.py` | 142 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\core\llm_manager.py` | 143 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\tex\tex_quality\style_profile.py` | 147 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\tex\tex_quality\quality_pipeline.py` | 148 |

### `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md`
*6 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\mathematical_engine.py` | 15 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\hol_lean_interface.py` | 16 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\pdf_rag_processor.py` | 17 |
| `ref_generique` | `agent-multiloop-Gabriel-local\memory\__init__.py` | 18 |
| `ref_generique` | `agent-multiloop-Gabriel-local\gabriel_mathematical.py` | 27 |
| `ref_generique` | `agent-multiloop-Gabriel-local\requirements.txt` | 29 |

### `agent-multiloop-Gabriel-local\SOLUTION_FINALE.txt`
*7 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\CINEMATIC_INTEGRATION_GUIDE.md` | 63 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CINEMATIC_MODE_SUMMARY.md` | 64 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CINEMATIC_EXAMPLES.py` | 65 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CINEMATIC_DEPLOYMENT.md` | 66 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md` | 207 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\ui\cli.py` | 235 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\ui\ask_gabriel.py` | 235 |

### `agent-multiloop-Gabriel-local\SOLUTION_SUMMARY_v5.3.txt`
*3 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\docker-compose.yml` | 31 |
| `ref_generique` | `agent-multiloop-Gabriel-local\gabriel_control.py` | 56 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 145 |

### `agent-multiloop-Gabriel-local\START_HERE.txt`
*10 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\docker-compose.yml` | 56 |
| `ref_generique` | `agent-multiloop-Gabriel-local\gabriel_launcher.py` | 58 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` | 60 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_FINAL_SOLUTION.txt` | 64 |
| `ref_generique` | `agent-multiloop-Gabriel-local\QUICK_REFERENCE.md` | 65 |
| `ref_generique` | `agent-multiloop-Gabriel-local\POWERSHELL_ISE_GUIDE.md` | 66 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_PORT_FIX_v5.3.md` | 67 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PORT_CLEANUP_IMPLEMENTATION.md` | 68 |
| `ref_generique` | `agent-multiloop-Gabriel-local\port_cleanup.py` | 71 |
| `ref_generique` | `agent-multiloop-Gabriel-local\gabriel_control.py` | 73 |

### `agent-multiloop-Gabriel-local\START_v5.0.txt`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v5_EXPLIQUE_SIMPLEMENT.txt` | 65 |

### `agent-multiloop-Gabriel-local\SYNTHESE_RSA_v2.2.md`
*3 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\test_rsa_capability.py` | 63 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v2.2_RSA_CAPABILITY.md` | 67 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CORRECTION_RSA_v2.2.md` | 71 |

### `agent-multiloop-Gabriel-local\SYNTHESE_ULTIME_v2.1.md`
*10 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\hol_lean_interface.py` | 21 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\mathematical_engine.py` | 22 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\pdf_rag_processor.py` | 23 |
| `ref_generique` | `agent-multiloop-Gabriel-local\memory\__init__.py` | 24 |
| `ref_generique` | `agent-multiloop-Gabriel-local\gabriel_mathematical.py` | 29 |
| `ref_generique` | `agent-multiloop-Gabriel-local\HOL4_SYSTEMATIC_PROOFS.md` | 39 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v2.1_RELEASE_NOTES.md` | 42 |
| `ref_generique` | `agent-multiloop-Gabriel-local\REPONSE_OUI_PREUVES_HOL4_SYSTEMATIQUES.md` | 45 |
| `ref_generique` | `agent-multiloop-Gabriel-local\EXEMPLE_GABRIEL_v2.1.py` | 48 |
| `ref_generique` | `agent-multiloop-Gabriel-local\requirements.txt` | 329 |

### `agent-multiloop-Gabriel-local\TEMPLATES_SUMMARY.md`
*6 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_01.thy` | 9 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_02.thy` | 10 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_100.thy` | 12 |
| `ref_generique` | `agent-multiloop-Gabriel-local\docker-compose.yml` | 23 |
| `ref_generique` | `agent-multiloop-Gabriel-local\main.py` | 190 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PROJECTS_TEMPLATES_GUIDE.md` | 231 |

### `agent-multiloop-Gabriel-local\TODO_ANALYSE.md`
*8 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\cost_manager.py` | 59 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\gabriel_llm_integration_safe.py` | 61 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\hol_lean_interface.py` | 62 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\hol_proof_corrector.py` | 63 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\isabelle_validator.py` | 65 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\llm_router.py` | 66 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\mathematical_engine.py` | 67 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\pdf_rag_processor.py` | 69 |

### `agent-multiloop-Gabriel-local\VALIDATION_HOL_INTEGRATION_COMPLETE.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\validation_hol_unifiee.thy` | 34 |
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 73 |

### `agent-multiloop-Gabriel-local\VALIDATION_HOL_UNIFIEE_ANALYSIS.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\validation_hol_unifiee.thy` | 1 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 91 |

### `agent-multiloop-Gabriel-local\VERIFICATION_COMPLETE_RESULTAT_FINAL.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\FINAL_RECONSTRUCTION_SUMMARY.txt` | 5 |
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 136 |

### `agent-multiloop-Gabriel-local\VERIFICATION_FINALE_SYNTHESE.txt`
*45 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\FINAL_RECONSTRUCTION_SUMMARY.txt` | 68 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GO_QUICK_START.md` | 73 |
| `ref_generique` | `agent-multiloop-Gabriel-local\QUICK_START_5_MINUTES.md` | 74 |
| `ref_generique` | `agent-multiloop-Gabriel-local\REPONSE_RAPIDE_RECONSTRUCTION.md` | 75 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md` | 78 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_IMAGE_ANALYSIS_COMPLETE_GUIDE.md` | 79 |
| `ref_generique` | `agent-multiloop-Gabriel-local\IMAGE_ANALYSIS_ANSWER_DIRECT.md` | 80 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GUIDE_ANALYSE_AVEC_CRITERES.md` | 81 |
| `ref_generique` | `agent-multiloop-Gabriel-local\COMMANDES_PRATIQUES_ANALYSE.md` | 82 |
| `ref_generique` | `agent-multiloop-Gabriel-local\QUICK_START_IMAGE_ANALYSIS.md` | 83 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GUIDE_RECONSTRUCTION_REDEMARRAGE.md` | 86 |
| `ref_generique` | `agent-multiloop-Gabriel-local\VALIDATION_HOL_UNIFIEE_ANALYSIS.md` | 89 |
| `ref_generique` | `agent-multiloop-Gabriel-local\VALIDATION_HOL_INTEGRATION_COMPLETE.md` | 90 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_VISION_QUICK_START.md` | 93 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` | 94 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_VISION_VERIFICATION_COMPLETE.md` | 95 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_COMPLETE_VISION_INTEGRATION.md` | 96 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v2.1_RELEASE_NOTES.md` | 99 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v2.2_RSA_CAPABILITY.md` | 100 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v3.0_MULTILOOP_VALIDATION.md` | 101 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v4.0_THEORY_MEMORY.md` | 102 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v5.0_LLM_ROUTING.md` | 103 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v5.1_SAFE_BUDGET.md` | 104 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v5.2_DEPLOYMENT_SUMMARY.md` | 105 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v5.2_HOL_FORMAL.md` | 106 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_v5_UPDATE_GUIDE.md` | 107 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` | 109 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md` | 110 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CONFIG_ENV_GUIDE.md` | 113 |
| `ref_generique` | `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` | 114 |
| `ref_generique` | `agent-multiloop-Gabriel-local\UTF8_ENCODING_FIX.md` | 115 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PYTEST_CHECKLIST.md` | 118 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PYTEST_EXECUTION_GUIDE.md` | 119 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PYTEST_INDEX.md` | 120 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PYTEST_LIST_COMPLETE.md` | 121 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PYTEST_SUMMARY.md` | 122 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CINEMATIC_DEPLOYMENT.md` | 125 |
| `ref_generique` | `agent-multiloop-Gabriel-local\DEPLOYMENT_CHECKLIST_v4.0.md` | 126 |
| `ref_generique` | `agent-multiloop-Gabriel-local\DEPLOYMENT_SUMMARY.md` | 127 |
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 139 |
| `ref_generique` | `agent-multiloop-Gabriel-local\main.py` | 140 |
| `ref_generique` | `agent-multiloop-Gabriel-local\requirements.txt` | 155 |
| `ref_generique` | `agent-multiloop-Gabriel-local\docker-compose.yml` | 157 |
| `ref_generique` | `agent-multiloop-Gabriel-local\RAPPORT_ANALYSE_DEPENDANCES.md` | 277 |
| `ref_generique` | `PLAN_ORGANISATION.md` | 278 |

### `agent-multiloop-Gabriel-local\VISUAL_SUMMARY_IMAGE_ANALYSIS.txt`
*11 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\complete_vision_system.py` | 31 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\production_validation_system.py` | 32 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\image_access_manager.py` | 33 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\vision_module.py` | 34 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\advanced_vision_module.py` | 35 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\gabriel_image_interface.py` | 36 |
| `ref_generique` | `agent-multiloop-Gabriel-local\IMAGE_ANALYSIS_ANSWER_DIRECT.md` | 150 |
| `ref_generique` | `agent-multiloop-Gabriel-local\QUICK_START_IMAGE_ANALYSIS.md` | 151 |
| `ref_generique` | `agent-multiloop-Gabriel-local\COPIER_COLLER_DIRECT.py` | 154 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PATCH_IMAGE_ANALYSIS_INTEGRATION.py` | 155 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GABRIEL_IMAGE_ANALYSIS_COMPLETE_GUIDE.md` | 158 |

### `agent-multiloop-Gabriel-local\apply_image_analysis_patch.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `Path()` | `agent-multiloop-Gabriel-local\src\ui\cli.py` | 178 |

### `agent-multiloop-Gabriel-local\apply_optimization.py`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\config.yaml` | 16 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\config_optimized.yaml` | 17 |

### `agent-multiloop-Gabriel-local\cognitive_pipeline_hol_unified.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 446 |

### `agent-multiloop-Gabriel-local\commande-gabriel\AIDE-MEMOIRE.txt`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\commande-gabriel\README.md` | 180 |

### `agent-multiloop-Gabriel-local\commande-gabriel\COMMANDES.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 10 |

### `agent-multiloop-Gabriel-local\config.yaml`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `yaml_chemin` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 62 |

### `agent-multiloop-Gabriel-local\deploy_image_analysis.py`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `Path()` | `agent-multiloop-Gabriel-local\src\gabriel_vision_integration.py` | 27 |
| `Path()` | `agent-multiloop-Gabriel-local\src\ui\cli.py` | 38 |

### `agent-multiloop-Gabriel-local\docs\ARCHITECTURE_USER.md`
*4 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\engines\abstraction\abstraction_layer.py` | 12 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\engines\generalization\generalizer.py` | 16 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\engines\theorem_discovery\discovery_loop.py` | 24 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\engines\concept_navigation\navigator.py` | 28 |

### `agent-multiloop-Gabriel-local\docs\PROMPT_CACHING_IMPLEMENTATION.md`
*5 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\prompt_cache_manager.py` | 284 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\gabriel_llm_integration_cache.py` | 285 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\llm_router_cache_extension.py` | 286 |
| `ref_generique` | `agent-multiloop-Gabriel-local\examples\example_prompt_caching.py` | 289 |
| `ref_generique` | `agent-multiloop-Gabriel-local\docs\PROMPT_CACHING_IMPLEMENTATION.md` | 292 |

### `agent-multiloop-Gabriel-local\docs\archive\CLAUDE_API_KEY_LOCALISATION.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\gabriel_llm_integration_v2.py` | 200 |
| `ref_generique` | `agent-multiloop-Gabriel-local\gabriel_mathematical.py` | 250 |

### `agent-multiloop-Gabriel-local\docs\archive\COGNITIVE_GAP_EXTENSION.md`
*3 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 190 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\spectral\gap_cognitive_model.py` | 202 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\spectral\gap_compute.py` | 206 |

### `agent-multiloop-Gabriel-local\docs\archive\CORRECTIONS_7eME_LOOP.md`
*6 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\multiloop\refinement_loop.py` | 53 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\multiloop\refinement_loop_fixed.py` | 54 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\core\pipeline.py` | 56 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\multiloop\slowmotion_trigger.py` | 89 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 278 |
| `ref_generique` | `agent-multiloop-Gabriel-local\memory\__init__.py` | 310 |

### `agent-multiloop-Gabriel-local\docs\archive\CORRECTION_TYPO_CLAUDE_KEY.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\gabriel_mathematical.py` | 118 |

### `agent-multiloop-Gabriel-local\docs\archive\FIX_NEGATIVE_NUMBERS.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\multiloop\request_decomposer.py` | 63 |

### `agent-multiloop-Gabriel-local\docs\archive\GABRIEL_v6.0_EXECUTIVE_SUMMARY.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `deploy_gabriel_v6.py` | 219 |

### `agent-multiloop-Gabriel-local\docs\archive\GABRIEL_v6.0_QUICK_REFERENCE.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `deploy_gabriel_v6.py` | 221 |

### `agent-multiloop-Gabriel-local\docs\archive\GABRIEL_v6.1_GAP_MIXED_HOL4.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\gabriel_llm_integration_v2.py` | 309 |

### `agent-multiloop-Gabriel-local\docs\archive\GAP_DEPLOYMENT.md`
*3 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\spectral\gap_cognitive_model.py` | 8 |
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 283 |
| `ref_generique` | `agent-multiloop-Gabriel-local\docs\archive\COGNITIVE_GAP_EXTENSION.md` | 315 |

### `agent-multiloop-Gabriel-local\docs\archive\GAP_FORMULA_CORRECTION.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\spectral\gap_solver_corrected.py` | 230 |

### `agent-multiloop-Gabriel-local\docs\archive\META_LEARNING_EXPERTISE.md`
*6 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\learning\debugging_expertise.py` | 281 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\learning\slowmotion_recorder.py` | 282 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\learning\meta_learning_integration.py` | 283 |
| `ref_generique` | `agent-multiloop-Gabriel-local\memory\__init__.py` | 453 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\core\pipeline.py` | 456 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\ui\cli.py` | 456 |

### `agent-multiloop-Gabriel-local\docs\archive\SECURITY_FIX.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\docs\archive\SECURITY_FIX.md` | 1 |

### `agent-multiloop-Gabriel-local\docs\archive\SECURITY_GUIDE.md`
*3 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\docs\archive\SECURITY_GUIDE.md` | 1 |
| `ref_generique` | `agent-multiloop-Gabriel-local\docs\archive\SECURITY_FIX.md` | 9 |
| `ref_generique` | `security_validator.py` | 39 |

### `agent-multiloop-Gabriel-local\docs\archive\SETUP_FINAL.md`
*5 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\docker-compose.yml` | 29 |
| `ref_generique` | `agent-multiloop-Gabriel-local\config.yaml` | 30 |
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 33 |
| `ref_generique` | `agent-multiloop-Gabriel-local\main.py` | 53 |
| `ref_generique` | `agent-multiloop-Gabriel-local\requirements.txt` | 55 |

### `agent-multiloop-Gabriel-local\docs\archive\SYNTHESE_COMPLETE.md`
*10 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\src\multiloop\refinement_loop_fixed.py` | 17 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\multiloop\slowmotion_trigger.py` | 21 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\learning\debugging_expertise.py` | 33 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\learning\slowmotion_recorder.py` | 41 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\learning\meta_learning_integration.py` | 48 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\multiloop\refinement_loop.py` | 184 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\core\pipeline.py` | 186 |
| `ref_generique` | `agent-multiloop-Gabriel-local\memory\__init__.py` | 193 |
| `ref_generique` | `agent-multiloop-Gabriel-local\docs\archive\CORRECTIONS_7eME_LOOP.md` | 202 |
| `ref_generique` | `agent-multiloop-Gabriel-local\docs\archive\META_LEARNING_EXPERTISE.md` | 203 |

### `agent-multiloop-Gabriel-local\docs\archive\test_result.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\docs\archive\test_result.md` | 91 |

### `agent-multiloop-Gabriel-local\env.example.txt`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\env.example.txt` | 6 |

### `agent-multiloop-Gabriel-local\examples\verif_p103_n27_CORRECT.thy`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `thy_import` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 1 |

### `agent-multiloop-Gabriel-local\examples\verif_p59_n17_CORRECTED.thy`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `thy_import` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 1 |

### `agent-multiloop-Gabriel-local\gabriel_launcher.py`
*3 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `agent-multiloop-Gabriel-local\port_cleanup.py` | 18 |
| `import_module` | `agent-multiloop-Gabriel-local\main_cli.py` | 51 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\logs` | 32 |

### `agent-multiloop-Gabriel-local\guide_utilisateur\README.md`
*7 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\QUICK_START_5_MINUTES.md` | 111 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md` | 112 |
| `ref_generique` | `agent-multiloop-Gabriel-local\GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md` | 113 |
| `ref_generique` | `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` | 114 |
| `ref_generique` | `agent-multiloop-Gabriel-local\PYTEST_SUMMARY.md` | 115 |
| `ref_generique` | `agent-multiloop-Gabriel-local\COMMANDS_COMPLETE_REFERENCE.md` | 116 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CONFIG_ENV_GUIDE.md` | 117 |

### `agent-multiloop-Gabriel-local\integration_mathematical.py`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `agent-multiloop-Gabriel-local\gabriel_mathematical.py` | 9 |
| `import_module` | `agent-multiloop-Gabriel-local\integration_mathematical.py` | 177 |

### `agent-multiloop-Gabriel-local\main.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\logs` | 102 |

### `agent-multiloop-Gabriel-local\main_cli.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\logs` | 136 |

### `agent-multiloop-Gabriel-local\port_cleanup.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `agent-multiloop-Gabriel-local\port_cleanup.py` | 10 |

### `agent-multiloop-Gabriel-local\question-definition.txt`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 1 |

### `agent-multiloop-Gabriel-local\quick_verification.py`
*9 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\src\mathematical_engine.py` | 45 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\src\hol_lean_interface.py` | 46 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\src\pdf_rag_processor.py` | 47 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\src\__init__.py` | 48 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\gabriel_mathematical.py` | 49 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\integration_mathematical.py` | 50 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\requirements.txt` | 52 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` | 56 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\CHECKLIST_FINAL.md` | 57 |

### `agent-multiloop-Gabriel-local\scripts\sync_theory_to_agent.py`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 24 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\scripts\isabelle_static_check.py` | 25 |

### `agent-multiloop-Gabriel-local\src\adapters\corpus\certainty_kernel.py`
*3 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 80 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\validation_hol_unifiee.thy` | 142 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\geometrie_spectre_premier.thy` | 187 |

### `agent-multiloop-Gabriel-local\src\adapters\corpus\thy_analyzer.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\scripts\isabelle_static_check.py` | 91 |

### `agent-multiloop-Gabriel-local\src\advanced_analysis_criteria.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `agent-multiloop-Gabriel-local\src\complete_vision_system.py` | 409 |

### `agent-multiloop-Gabriel-local\src\complete_validation_integration.py`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `agent-multiloop-Gabriel-local\src\complete_vision_system.py` | 19 |
| `import_module` | `agent-multiloop-Gabriel-local\src\parametric_validation_module.py` | 28 |

### `agent-multiloop-Gabriel-local\src\complete_vision_system.py`
*3 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `agent-multiloop-Gabriel-local\src\image_access_manager.py` | 29 |
| `import_module` | `agent-multiloop-Gabriel-local\src\vision_module.py` | 36 |
| `import_module` | `agent-multiloop-Gabriel-local\src\advanced_vision_module.py` | 42 |

### `agent-multiloop-Gabriel-local\src\core\config.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\config.yaml` | 72 |

### `agent-multiloop-Gabriel-local\src\core\llm_manager.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` | 38 |

### `agent-multiloop-Gabriel-local\src\gabriel_image_interface.py`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `agent-multiloop-Gabriel-local\src\complete_validation_integration.py` | 22 |
| `import_module` | `agent-multiloop-Gabriel-local\src\production_validation_system.py` | 28 |

### `agent-multiloop-Gabriel-local\src\image_discovery_system.py`
*5 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `Path()` | `C:\Users` | 183 |
| `Path()` | `agent-multiloop-Gabriel-local\src` | 185 |
| `Path()` | `agent-multiloop-Gabriel-local` | 186 |
| `Path()` | `agent-multiloop-Gabriel-local\data` | 191 |
| `Path()` | `C:\theorie-mathematique` | 192 |

### `agent-multiloop-Gabriel-local\src\multiloop\domain_classifier.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 64 |

### `agent-multiloop-Gabriel-local\src\multiloop\domain_gate.py`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `agent-multiloop-Gabriel-local\src\multiloop\domain_classifier.py` | 17 |
| `import_module` | `agent-multiloop-Gabriel-local\src\multiloop\gabriel_domain_config.py` | 25 |

### `agent-multiloop-Gabriel-local\src\multiloop\gabriel_domain_config.py`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 41 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\geometrie_spectre_premier.thy` | 42 |

### `agent-multiloop-Gabriel-local\src\spectral\tchebychev_savard_pipeline.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `agent-multiloop-Gabriel-local\src\spectral\prime_table.py` | 15 |

### `agent-multiloop-Gabriel-local\test_rsa_capability.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `agent-multiloop-Gabriel-local\gabriel_mathematical.py` | 93 |

### `agent-multiloop-Gabriel-local\test_spectral_gabriel.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `agent-multiloop-Gabriel-local\src\core\spectral_core.py` | 26 |

### `agent-multiloop-Gabriel-local\tests\test_ask_gabriel.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 106 |

### `agent-multiloop-Gabriel-local\tests\test_audit_store.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 194 |

### `agent-multiloop-Gabriel-local\tests\test_banque_qr_sentinelle.py`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\memory\banque_qr_methode_spectrale.md` | 17 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 191 |

### `agent-multiloop-Gabriel-local\tests\test_blocs_v343.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 12 |

### `agent-multiloop-Gabriel-local\tests\test_cartouche_uniforme_ascii.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 6 |

### `agent-multiloop-Gabriel-local\tests\test_ci_regex_and_env_placeholder_fix.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `tests` | 32 |

### `agent-multiloop-Gabriel-local\tests\test_composite_absurdity.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 171 |

### `agent-multiloop-Gabriel-local\tests\test_conversational_mode.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\src\core\pipeline.py` | 88 |

### `agent-multiloop-Gabriel-local\tests\test_critic_vocab_and_gestionnaire_fix.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\src\core\llm_manager.py` | 133 |

### `agent-multiloop-Gabriel-local\tests\test_dictionnaire_rag.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `memory` | 7 |

### `agent-multiloop-Gabriel-local\tests\test_domaine_sommes_XIA_v339.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 27 |

### `agent-multiloop-Gabriel-local\tests\test_env_config.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\CONFIG_ENV_GUIDE.md` | 100 |

### `agent-multiloop-Gabriel-local\tests\test_extract_numbers_unicode_v346.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\src\engines\abstraction\abstraction_layer.py` | 54 |

### `agent-multiloop-Gabriel-local\tests\test_image_command_windows_routing.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\docker-compose.yml` | 107 |

### `agent-multiloop-Gabriel-local\tests\test_isabelle_fixes_bugs_9_10.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 32 |

### `agent-multiloop-Gabriel-local\tests\test_isabelle_fixes_v321.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 28 |

### `agent-multiloop-Gabriel-local\tests\test_isabelle_rsp_non_zero_witness.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 26 |

### `agent-multiloop-Gabriel-local\tests\test_methode_spectral_healthcheck.py`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `agent-multiloop-Gabriel-local\theories\verify_thy_structure.py` | 18 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 16 |

### `agent-multiloop-Gabriel-local\tests\test_paths_resolution_container_fix.py`
*4 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `tests` | 40 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\CONFIG_ENV_GUIDE.md` | 57 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 107 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\docker-compose.yml` | 128 |

### `agent-multiloop-Gabriel-local\tests\test_philippe_three_categories_v329.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 66 |

### `agent-multiloop-Gabriel-local\tests\test_psi_savard_pont_zeta_v331.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 24 |

### `agent-multiloop-Gabriel-local\tests\test_restore_methode_spectral_0f277b5.py`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 14 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 15 |

### `agent-multiloop-Gabriel-local\tests\test_section_XI_XII_integration.py`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 23 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\scripts\isabelle_static_check.py` | 197 |

### `agent-multiloop-Gabriel-local\tests\test_section_xiii_professionnelle_v332.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 30 |

### `agent-multiloop-Gabriel-local\tests\test_section_xiii_rag_v333.py`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` | 236 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 55 |

### `agent-multiloop-Gabriel-local\tests\test_spectral_family_foundations_v335.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 34 |

### `agent-multiloop-Gabriel-local\tests\test_timeout_and_extensions_v320.py`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\config.yaml` | 25 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 113 |

### `agent-multiloop-Gabriel-local\tests\test_ui_pro_banner_and_memoire.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` | 52 |

### `agent-multiloop-Gabriel-local\tests\test_validation16_savard_and_build_workflow.py`
*3 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 41 |
| `chemin_litteral` | `.github\workflows\build.yml` | 223 |
| `chemin_litteral` | `.github` | 227 |

### `agent-multiloop-Gabriel-local\tests\test_verify_thy_structure.py`
*3 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `agent-multiloop-Gabriel-local\theories\verify_thy_structure.py` | 24 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\verify_thy_structure.py` | 22 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 340 |

### `agent-multiloop-Gabriel-local\tests\test_workflow_isabelle_syntax.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `.github\workflows\build.yml` | 95 |

### `agent-multiloop-Gabriel-local\theories\methode_spectral.thy`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `thy_ref_croisee` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 8 |

### `agent-multiloop-Gabriel-local\theories\methode_spectral_de.thy`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `thy_ref_croisee` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 3 |

### `agent-multiloop-Gabriel-local\theories\methode_spectral_en.thy`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `thy_ref_croisee` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 3 |

### `agent-multiloop-Gabriel-local\theories\methode_spectral_es.thy`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `thy_ref_croisee` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 3 |

### `agent-multiloop-Gabriel-local\theories\methode_spectral_ja.thy`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `thy_ref_croisee` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 3 |

### `agent-multiloop-Gabriel-local\theories\methode_spectral_pt.thy`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `thy_ref_croisee` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 3 |

### `agent-multiloop-Gabriel-local\theories\methode_spectral_ru.thy`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `thy_ref_croisee` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 3 |

### `agent-multiloop-Gabriel-local\theories\methode_spectral_zh.thy`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `thy_ref_croisee` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 3 |

### `agent-multiloop-Gabriel-local\theories\tex\README_pdf.md`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 147 |
| `ref_generique` | `README.md` | 148 |

### `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `json_chemin` | `agent-multiloop-Gabriel-local\scripts\tex_healthcheck.py` | 4019 |

### `agent-multiloop-Gabriel-local\theories\tex\tex_quality\quality_pipeline.py`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\tex\tex_quality\README.md` | 69 |
| `chemin_litteral` | `agent-multiloop-Gabriel-local\scripts\tex_healthcheck.py` | 585 |

### `agent-multiloop-Gabriel-local\theories\validation_hol_unifiee.thy`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `thy_import` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 16 |

### `declaration_securite.md`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `SECURITY.md` | 3 |

### `find_debugger.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `open_fichier` | `agent-multiloop-Gabriel-local\src\core\pipeline.py` | 5 |

### `fix_corrections.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 10 |

### `fix_debugger.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `open_fichier` | `agent-multiloop-Gabriel-local\src\core\pipeline.py` | 8 |

### `fix_line_2605.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 7 |

### `fix_theoretical_patterns.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `agent-multiloop-Gabriel-local\src\multiloop\request_decomposer.py` | 7 |

### `frontend\src\constants\testIds\auth.js`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `frontend\src\constants\testIds\index.js` | 2 |

### `frontend\src\constants\testIds\home.js`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `frontend\src\constants\testIds\auth.js` | 2 |

### `frontend\tailwind.config.js`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `frontend\public\index.html` | 6 |

### `gabriel_repo_mapper.py`
*2 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `Path()` | `.` | 100 |
| `base_donnees` | `.` | 123 |

### `memory\PRD.md`
*17 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `ref_generique` | `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` | 7 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\engines\question_graphs.py` | 62 |
| `ref_generique` | `agent-multiloop-Gabriel-local\CONFIG_ENV_GUIDE.md` | 334 |
| `ref_generique` | `agent-multiloop-Gabriel-local\docker-compose.yml` | 386 |
| `ref_generique` | `agent-multiloop-Gabriel-local\main_cli.py` | 388 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\ui\cli.py` | 403 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\ui\ci_status.py` | 404 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\ui\debug_session.py` | 405 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\visualization\curves.py` | 407 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\visualization\ascii_renderer.py` | 408 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\visualization\rich_renderer.py` | 409 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\visualization\png_renderer.py` | 410 |
| `ref_generique` | `agent-multiloop-Gabriel-local\HOL_ISABELLE_FIX.md` | 808 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\adapters\hol_integration.py` | 808 |
| `ref_generique` | `agent-multiloop-Gabriel-local\src\spectral\hol_script_generator.py` | 808 |
| `ref_generique` | `agent-multiloop-Gabriel-local\examples\verif_p103_n27_CORRECT.thy` | 808 |
| `ref_generique` | `README.md` | 840 |

### `memory\gestionnaire_erreurs.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `memory\error_cache\errors.json` | 68 |

### `memory\theory_axioms_manager.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `chemin_litteral` | `memory\directives_theorie_savard.md` | 51 |

### `src\core\gabriel_comparaison_asymetrique.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `memory\comparaison_asymetrique_ordonnee.py` | 17 |

### `src\core\integrateur_memoire.py`
*5 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `memory\memoire_conceptuelle.py` | 20 |
| `import_module` | `memory\memoire_technique.py` | 28 |
| `import_module` | `memory\gestionnaire_erreurs.py` | 38 |
| `import_module` | `src\core\detecteur_asymetrique_ordonnee.py` | 49 |
| `import_module` | `src\core\gabriel_comparaison_asymetrique.py` | 50 |

### `test_imports.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `src\core\detecteur_asymetrique_ordonnee.py` | 11 |

### `test_systeme_memoire_complet.py`
*1 lien(s) sortant(s)*

| Type de lien | Fichier cible | Ligne |
|-------------|---------------|-------|
| `import_module` | `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` | 51 |

## 5. Références potentiellement non résolues

| Fichier source | Référence | Type | Ligne |
|---------------|-----------|------|-------|
| `.emergent\cron\dispatch_webhook.sh` | `The` | `shell_appel` | 3 |
| `.emergent\cron\dispatch_webhook.sh` | `set` | `shell_appel` | 4 |
| `.emergent\cron\dispatch_webhook.sh` | `Fire` | `shell_appel` | 14 |
| `.emergent\cron\dispatch_webhook.sh` | `if` | `shell_appel` | 15 |
| `.emergent\cron\dispatch_webhook.sh` | `Stop` | `shell_appel` | 24 |
| `.emergent\cron\dispatch_webhook.sh` | `v` | `shell_appel` | 34 |
| `.emergent\cron\dispatch_webhook.sh` | `read_secret` | `shell_appel` | 43 |
| `.emergent\cron\dispatch_webhook.sh` | `RUN_ID` | `shell_appel` | 53 |
| `.emergent\cron\dispatch_webhook.sh` | `HTTP_STATUS` | `shell_appel` | 61 |
| `.emergent\cron\watch_crons.sh` | `It` | `shell_appel` | 5 |
| `.emergent\cron\watch_crons.sh` | `set` | `shell_appel` | 6 |
| `.emergent\cron\watch_crons.sh` | `hash_file` | `shell_appel` | 14 |
| `.emergent\cron\watch_crons.sh` | `curl` | `shell_appel` | 31 |
| `.emergent\cron\webhook_crond.sh` | `Before` | `shell_appel` | 5 |
| `.emergent\cron\webhook_crond.sh` | `set` | `shell_appel` | 8 |
| `.emergent\cron\webhook_crond.sh` | `if` | `shell_appel` | 17 |
| `.emergent\cron\webhook_crond.sh` | `Debian` | `shell_appel` | 27 |
| `.emergent\summary.txt` | `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local` | `ref_generique` | 36 |
| `.emergent\summary.txt` | `emrgent.sh` | `ref_generique` | 586 |
| `.emergent\summary.txt` | `/dist/` | `ref_generique` | 750 |
| `.emergent\summary.txt` | `./theories/methode_spectral.thy` | `ref_generique` | 1009 |
| `.emergent\summary.txt` | `./theories/methode_spectral.thy`` | `ref_generique` | 1013 |
| `.emergent\summary.txt` | `attestation_report.txt` | `ref_generique` | 1031 |
| `.emergent\summary.txt` | `XXX.thy` | `ref_generique` | 1033 |
| `.emergent\summary.txt` | `./XXX` | `ref_generique` | 1034 |
| `.emergent\summary.txt` | `SHA256SUMS.txt` | `ref_generique` | 1151 |
| `.emergent\summary.txt` | `Methode_spectral.thy` | `ref_generique` | 1291 |
| `.emergent\summary.txt` | `emergent.sh` | `ref_generique` | 1339 |
| `activation_memoire.py` | `error_cache/errors.json` | `chemin_litteral` | 23 |
| `agent-multiloop-Gabriel-local\00_START_HERE_IMAGE_ANALYSIS.md` | `/home/.../image.png` | `ref_generique` | 151 |
| `agent-multiloop-Gabriel-local\00_START_HERE_IMAGE_ANALYSIS.md` | `./images/figure.png` | `ref_generique` | 152 |
| `agent-multiloop-Gabriel-local\00_START_HERE_IMAGE_ANALYSIS.md` | `./test.png` | `ref_generique` | 305 |
| `agent-multiloop-Gabriel-local\00_START_HERE_IMAGE_ANALYSIS.md` | `/nonexistent/image.png` | `ref_generique` | 313 |
| `agent-multiloop-Gabriel-local\apply_image_analysis_patch.py` | `Applique les 3 modifications à cli.py` | `chemin_litteral` | 12 |
| `agent-multiloop-Gabriel-local\apply_image_analysis_patch.py` | `  2. python src/ui/cli.py` | `chemin_litteral` | 190 |
| `agent-multiloop-Gabriel-local\backend\multiloop_backend.py` | `data/multiloop_results/latest.json` | `chemin_litteral` | 208 |
| `agent-multiloop-Gabriel-local\CHECKLIST_FINAL.md` | `os.env` | `ref_generique` | 86 |
| `agent-multiloop-Gabriel-local\CHECKLIST_FINAL.md` | `riemann_spectral.thy` | `ref_generique` | 117 |
| `agent-multiloop-Gabriel-local\CHECKLIST_FINAL.md` | `pdf_index.json` | `ref_generique` | 125 |
| `agent-multiloop-Gabriel-local\CHECKLIST_FINAL.md` | `config_mathematical.env` | `ref_generique` | 129 |
| `agent-multiloop-Gabriel-local\CHECKLIST_FINAL.md` | `README_MATHEMATICAL_v2.md` | `ref_generique` | 132 |
| `agent-multiloop-Gabriel-local\CHECKLIST_FINAL.md` | `/api/query` | `ref_generique` | 197 |
| `agent-multiloop-Gabriel-local\CHECKLIST_FINAL.md` | `//raw.githubusercontent.com/leanprover/elan/master/elan-init.sh` | `ref_generique` | 299 |
| `agent-multiloop-Gabriel-local\CINEMATIC_DEPLOYMENT.md` | `/home/agent/app/src/ui/` | `ref_generique` | 26 |
| `agent-multiloop-Gabriel-local\CLAUDE_BUDGET_GUIDE.md` | `//console.anthropic.com/usage` | `ref_generique` | 204 |
| `agent-multiloop-Gabriel-local\cognitive_pipeline_hol_unified.py` | `/home/agent/app` | `Path()` | 445 |
| `agent-multiloop-Gabriel-local\cognitive_pipeline_hol_unified.py` | `hol_unified_validation.db` | `chemin_litteral` | 447 |
| `agent-multiloop-Gabriel-local\COMMANDS_COMPLETE_REFERENCE.md` | `//localhost` | `ref_generique` | 87 |
| `agent-multiloop-Gabriel-local\COMMANDS_COMPLETE_REFERENCE.md` | `/theories/projects/` | `ref_generique` | 151 |
| `agent-multiloop-Gabriel-local\COMMANDS_COMPLETE_REFERENCE.md` | `/theories/projects/txt/` | `ref_generique` | 157 |
| `agent-multiloop-Gabriel-local\COMMANDS_COMPLETE_REFERENCE.md` | `/theories/projects/tex/` | `ref_generique` | 163 |
| `agent-multiloop-Gabriel-local\COMMANDS_COMPLETE_REFERENCE.md` | `/theories/projects/projet_uni_car_savard_01.thy` | `ref_generique` | 179 |
| `agent-multiloop-Gabriel-local\COMMANDS_COMPLETE_REFERENCE.md` | `/theories` | `ref_generique` | 189 |
| `agent-multiloop-Gabriel-local\COMMANDS_COMPLETE_REFERENCE.md` | `/theories/projects/exemple.thy` | `ref_generique` | 242 |
| `agent-multiloop-Gabriel-local\COMMANDS_COMPLETE_REFERENCE.md` | `/theories/projects/projet_uni_car_savard_26.thy` | `ref_generique` | 325 |
| `agent-multiloop-Gabriel-local\COMMANDS_COMPLETE_REFERENCE.md` | `/theories/projects/tex` | `ref_generique` | 335 |
| `agent-multiloop-Gabriel-local\COMMANDS_COMPLETE_REFERENCE.md` | `/theories/projects/projet_uni_car_savard_` | `ref_generique` | 346 |
| `agent-multiloop-Gabriel-local\COMMANDS_COMPLETE_REFERENCE.md` | `/home/agent/app/data` | `ref_generique` | 461 |
| `agent-multiloop-Gabriel-local\COMMANDS_COMPLETE_REFERENCE.md` | `/home/agent/app/` | `ref_generique` | 466 |
| `agent-multiloop-Gabriel-local\COMPLETE_INTEGRATION_INSTRUCTIONS.md` | `./test.png` | `ref_generique` | 399 |
| `agent-multiloop-Gabriel-local\config.yaml` | `/theories` | `yaml_chemin` | 97 |
| `agent-multiloop-Gabriel-local\config.yaml` | `/workspace/corpus_actions/pdf` | `yaml_chemin` | 98 |
| `agent-multiloop-Gabriel-local\config.yaml` | `/workspace/corpus_actions/tex` | `yaml_chemin` | 99 |
| `agent-multiloop-Gabriel-local\config.yaml` | `/home/agent/app/data` | `yaml_chemin` | 100 |
| `agent-multiloop-Gabriel-local\config.yaml` | `/opt/Isabelle2025-2` | `yaml_chemin` | 105 |
| `agent-multiloop-Gabriel-local\config.yaml` | `/home/agent/app/logs` | `yaml_chemin` | 126 |
| `agent-multiloop-Gabriel-local\CONFIG_ENV_GUIDE.md` | `/home/agent/app/.env` | `ref_generique` | 12 |
| `agent-multiloop-Gabriel-local\CONFIG_ENV_GUIDE.md` | `./.env:/home/agent/app/.env:ro`.` | `ref_generique` | 19 |
| `agent-multiloop-Gabriel-local\CONFIG_ENV_GUIDE.md` | `Emergent.sh` | `ref_generique` | 120 |
| `agent-multiloop-Gabriel-local\CONFIG_ENV_GUIDE.md` | `//console.anthropic.com/settings/keys` | `ref_generique` | 141 |
| `agent-multiloop-Gabriel-local\deploy_image_analysis.py` | `  ⚠️ Manual patching required - see COMPLETE_INTEGRATION_INSTRUCTIONS.md` | `chemin_litteral` | 50 |
| `agent-multiloop-Gabriel-local\DEPLOYMENT_CHECKLIST_v4.0.md` | `/query` | `ref_generique` | 39 |
| `agent-multiloop-Gabriel-local\DEPLOYMENT_CHECKLIST_v4.0.md` | `/sync/universestaucarre` | `ref_generique` | 44 |
| `agent-multiloop-Gabriel-local\DEPLOYMENT_CHECKLIST_v4.0.md` | `/isabelle/verify` | `ref_generique` | 49 |
| `agent-multiloop-Gabriel-local\DEPLOYMENT_CHECKLIST_v4.0.md` | `/data/isabelle-results/` | `ref_generique` | 51 |
| `agent-multiloop-Gabriel-local\DEPLOYMENT_CHECKLIST_v4.0.md` | `/health` | `ref_generique` | 54 |
| `agent-multiloop-Gabriel-local\DEPLOYMENT_CHECKLIST_v4.0.md` | `/stream` | `ref_generique` | 58 |
| `agent-multiloop-Gabriel-local\DEPLOYMENT_CHECKLIST_v4.0.md` | `/theories` | `ref_generique` | 82 |
| `agent-multiloop-Gabriel-local\DEPLOYMENT_CHECKLIST_v4.0.md` | `/output/` | `ref_generique` | 86 |
| `agent-multiloop-Gabriel-local\DEPLOYMENT_CHECKLIST_v4.0.md` | `/tmp/.X11-unix` | `ref_generique` | 95 |
| `agent-multiloop-Gabriel-local\DEPLOYMENT_CHECKLIST_v4.0.md` | `README_v4.0.md` | `ref_generique` | 105 |
| `agent-multiloop-Gabriel-local\DEPLOYMENT_CHECKLIST_v4.0.md` | `//localhost` | `ref_generique` | 125 |
| `agent-multiloop-Gabriel-local\DEPLOYMENT_CHECKLIST_v4.0.md` | `/data/universestaucarre-sync/` | `ref_generique` | 171 |
| `agent-multiloop-Gabriel-local\DEPLOYMENT_CHECKLIST_v4.0.md` | `/theories/generated/` | `ref_generique` | 199 |
| `agent-multiloop-Gabriel-local\DEPLOYMENT_SUMMARY.md` | `config_mathematical.env` | `ref_generique` | 54 |
| `agent-multiloop-Gabriel-local\DEPLOYMENT_SUMMARY.md` | `//docs.sympy.org/` | `ref_generique` | 265 |
| `agent-multiloop-Gabriel-local\DEPLOYMENT_SUMMARY.md` | `//mpmath.org/` | `ref_generique` | 266 |
| `agent-multiloop-Gabriel-local\DEPLOYMENT_SUMMARY.md` | `//github.com/HOL-Theorem-Prover/HOL` | `ref_generique` | 267 |
| `agent-multiloop-Gabriel-local\DEPLOYMENT_SUMMARY.md` | `//lean-lang.org/` | `ref_generique` | 268 |
| `agent-multiloop-Gabriel-local\DEPLOYMENT_SUMMARY.md` | `//pari.math.u-bordeaux.fr/` | `ref_generique` | 269 |
| `agent-multiloop-Gabriel-local\docker-compose.yml` | `/theories` | `yaml_chemin` | 130 |
| `agent-multiloop-Gabriel-local\docs\ARCHITECTURE_USER.md` | `concept_extractor.py` | `ref_generique` | 12 |
| `agent-multiloop-Gabriel-local\docs\ARCHITECTURE_USER.md` | `abstraction_rules.py` | `ref_generique` | 12 |
| `agent-multiloop-Gabriel-local\docs\ARCHITECTURE_USER.md` | `pattern_matcher.py` | `ref_generique` | 16 |
| `agent-multiloop-Gabriel-local\docs\ARCHITECTURE_USER.md` | `generalization_rules.py` | `ref_generique` | 16 |
| `agent-multiloop-Gabriel-local\docs\ARCHITECTURE_USER.md` | `proof_planner.py` | `ref_generique` | 20 |
| `agent-multiloop-Gabriel-local\docs\ARCHITECTURE_USER.md` | `goal_analyzer.py` | `ref_generique` | 20 |
| `agent-multiloop-Gabriel-local\docs\ARCHITECTURE_USER.md` | `strategy_selector.py` | `ref_generique` | 20 |
| `agent-multiloop-Gabriel-local\docs\ARCHITECTURE_USER.md` | `conjecture_generator.py` | `ref_generique` | 24 |
| `agent-multiloop-Gabriel-local\docs\ARCHITECTURE_USER.md` | `conjecture_filter.py` | `ref_generique` | 24 |
| `agent-multiloop-Gabriel-local\docs\ARCHITECTURE_USER.md` | `graph_builder.py` | `ref_generique` | 28 |
| `agent-multiloop-Gabriel-local\docs\ARCHITECTURE_USER.md` | `query_mapper.py` | `ref_generique` | 28 |
| `agent-multiloop-Gabriel-local\docs\ARCHITECTURE_USER.md` | `/theories` | `ref_generique` | 77 |
| `agent-multiloop-Gabriel-local\docs\archive\CLAUDE_API_KEY_LOCALISATION.md` | `config_mathematical.env` | `ref_generique` | 29 |
| `agent-multiloop-Gabriel-local\docs\archive\CLAUDE_API_KEY_LOCALISATION.md` | `//console.anthropic.com/` | `ref_generique` | 166 |
| `agent-multiloop-Gabriel-local\docs\archive\COGNITIVE_GAP_EXTENSION.md` | `gap_solver.py` | `ref_generique` | 204 |
| `agent-multiloop-Gabriel-local\docs\archive\CORRECTION_TYPO_CLAUDE_KEY.md` | `test_claude_api_key_location.py` | `ref_generique` | 137 |
| `agent-multiloop-Gabriel-local\docs\archive\CORRECTIONS_7eME_LOOP.md` | `pipeline_fixed.py` | `ref_generique` | 57 |
| `agent-multiloop-Gabriel-local\docs\archive\GAP_DEPLOYMENT.md` | `gap_solver.py` | `ref_generique` | 9 |
| `agent-multiloop-Gabriel-local\docs\archive\GAP_DEPLOYMENT.md` | `/theories` | `ref_generique` | 58 |
| `agent-multiloop-Gabriel-local\docs\archive\GAP_FORMULA_CORRECTION.md` | `gap_solver.py` | `ref_generique` | 5 |
| `agent-multiloop-Gabriel-local\docs\archive\LLM_MANAGER_v2_MIGRATION.md` | `//localhost` | `ref_generique` | 113 |
| `agent-multiloop-Gabriel-local\docs\archive\META_LEARNING_EXPERTISE.md` | `MetaLearningManager.sh` | `ref_generique` | 156 |
| `agent-multiloop-Gabriel-local\docs\archive\SECURITY_FIX.md` | `//platform.openai.com/api-keys` | `ref_generique` | 20 |
| `agent-multiloop-Gabriel-local\docs\archive\SECURITY_FIX.md` | `non-.env` | `ref_generique` | 69 |
| `agent-multiloop-Gabriel-local\docs\archive\SECURITY_FIX.md` | `./backup` | `ref_generique` | 70 |
| `agent-multiloop-Gabriel-local\docs\archive\SECURITY_FIX.md` | `//www.gitguardian.com/` | `ref_generique` | 189 |
| `agent-multiloop-Gabriel-local\docs\archive\SECURITY_FIX.md` | `/path/to/repo` | `ref_generique` | 194 |
| `agent-multiloop-Gabriel-local\docs\archive\SECURITY_FIX.md` | `//github.com/2racinede4carreunivers-dev/...` | `ref_generique` | 222 |
| `agent-multiloop-Gabriel-local\docs\archive\SECURITY_FIX.md` | `//api.github.com/repos/.../.../contents/.env` | `ref_generique` | 355 |
| `agent-multiloop-Gabriel-local\docs\archive\SECURITY_GUIDE.md` | `//platform.openai.com/api-keys` | `ref_generique` | 20 |
| `agent-multiloop-Gabriel-local\docs\archive\SECURITY_GUIDE.md` | `//platform.openai.com/account/usage` | `ref_generique` | 137 |
| `agent-multiloop-Gabriel-local\docs\archive\SECURITY_GUIDE.md` | `//github.com/settings/tokens` | `ref_generique` | 142 |
| `agent-multiloop-Gabriel-local\docs\archive\SECURITY_GUIDE.md` | `//github.com/settings/security-log` | `ref_generique` | 328 |
| `agent-multiloop-Gabriel-local\docs\archive\SECURITY_GUIDE.md` | `//api.github.com/.../contents/.env` | `ref_generique` | 353 |
| `agent-multiloop-Gabriel-local\docs\archive\SYNTHESE_COMPLETE.md` | `pipeline_fixed.py` | `ref_generique` | 25 |
| `agent-multiloop-Gabriel-local\docs\archive\SYNTHESE_COMPLETE.md` | `dbg_a1b2c3d4.json` | `ref_generique` | 60 |
| `agent-multiloop-Gabriel-local\docs\archive\SYNTHESE_COMPLETE.md` | `Pipeline_fixed.py` | `ref_generique` | 267 |
| `agent-multiloop-Gabriel-local\docs\archive\test_result.md` | `file_path.py` | `ref_generique` | 22 |
| `agent-multiloop-Gabriel-local\docs\archive\test_result.md` | `task_result.md` | `ref_generique` | 76 |
| `agent-multiloop-Gabriel-local\docs\geometrie_spectre_premiers.tex` | `inputenc` | `latex_inclusion` | 12 |
| `agent-multiloop-Gabriel-local\docs\geometrie_spectre_premiers.tex` | `fontenc` | `latex_inclusion` | 13 |
| `agent-multiloop-Gabriel-local\docs\geometrie_spectre_premiers.tex` | `babel` | `latex_inclusion` | 14 |
| `agent-multiloop-Gabriel-local\docs\geometrie_spectre_premiers.tex` | `lmodern` | `latex_inclusion` | 15 |
| `agent-multiloop-Gabriel-local\docs\geometrie_spectre_premiers.tex` | `amsmath, amssymb, amsthm` | `latex_inclusion` | 16 |
| `agent-multiloop-Gabriel-local\docs\geometrie_spectre_premiers.tex` | `graphicx` | `latex_inclusion` | 17 |
| `agent-multiloop-Gabriel-local\docs\geometrie_spectre_premiers.tex` | `booktabs, longtable, array` | `latex_inclusion` | 18 |
| `agent-multiloop-Gabriel-local\docs\geometrie_spectre_premiers.tex` | `hyperref` | `latex_inclusion` | 19 |
| `agent-multiloop-Gabriel-local\docs\geometrie_spectre_premiers.tex` | `xcolor` | `latex_inclusion` | 20 |
| `agent-multiloop-Gabriel-local\docs\geometrie_spectre_premiers.tex` | `geometry` | `latex_inclusion` | 21 |
| `agent-multiloop-Gabriel-local\docs\geometrie_spectre_premiers.tex` | `fancyhdr` | `latex_inclusion` | 22 |
| `agent-multiloop-Gabriel-local\docs\PROMPT_CACHING_IMPLEMENTATION.md` | `//docs.anthropic.com/en/docs/build-a-Claude-app/prompt-caching` | `ref_generique` | 358 |
| `agent-multiloop-Gabriel-local\docs\PROMPT_CACHING_IMPLEMENTATION.md` | `//examples.com/cache-analysis` | `ref_generique` | 359 |
| `agent-multiloop-Gabriel-local\docs\PROMPT_CACHING_IMPLEMENTATION.md` | `//github.com/...` | `ref_generique` | 360 |
| `agent-multiloop-Gabriel-local\docs\psi_savard_comparison.tex` | `inputenc` | `latex_inclusion` | 2 |
| `agent-multiloop-Gabriel-local\docs\psi_savard_comparison.tex` | `fontenc` | `latex_inclusion` | 3 |
| `agent-multiloop-Gabriel-local\docs\psi_savard_comparison.tex` | `babel` | `latex_inclusion` | 4 |
| `agent-multiloop-Gabriel-local\docs\psi_savard_comparison.tex` | `amsmath,amssymb,booktabs,pgfplots` | `latex_inclusion` | 5 |
| `agent-multiloop-Gabriel-local\env.example.txt` | `//developer.wolframalpha.com/access` | `ref_generique` | 14 |
| `agent-multiloop-Gabriel-local\env.example.txt` | `//host.docker.internal` | `ref_generique` | 19 |
| `agent-multiloop-Gabriel-local\env.example.txt` | `/theories` | `ref_generique` | 27 |
| `agent-multiloop-Gabriel-local\env.example.txt` | `/workspace/corpus_actions/pdf` | `ref_generique` | 28 |
| `agent-multiloop-Gabriel-local\env.example.txt` | `/workspace/corpus_actions/tex` | `ref_generique` | 29 |
| `agent-multiloop-Gabriel-local\FILES_v5.0.md` | `//localhost` | `ref_generique` | 48 |
| `agent-multiloop-Gabriel-local\FINAL_300_TEMPLATES_SUMMARY.md` | `/theories/projects/` | `ref_generique` | 59 |
| `agent-multiloop-Gabriel-local\FINAL_300_TEMPLATES_SUMMARY.md` | `/theories/projects/txt/` | `ref_generique` | 60 |
| `agent-multiloop-Gabriel-local\FINAL_300_TEMPLATES_SUMMARY.md` | `/theories/projects/tex/` | `ref_generique` | 61 |
| `agent-multiloop-Gabriel-local\FINAL_300_TEMPLATES_SUMMARY.md` | `/theories/projects` | `ref_generique` | 64 |
| `agent-multiloop-Gabriel-local\FINAL_300_TEMPLATES_SUMMARY.md` | `//localhost` | `ref_generique` | 230 |
| `agent-multiloop-Gabriel-local\FINAL_300_TEMPLATES_SUMMARY.md` | `/theories/projects/projet_uni_car_savard_01.thy` | `ref_generique` | 233 |
| `agent-multiloop-Gabriel-local\FINAL_300_TEMPLATES_SUMMARY.md` | `/theories/projects/txt/projet_uni_car_savard_01.txt` | `ref_generique` | 234 |
| `agent-multiloop-Gabriel-local\FINAL_300_TEMPLATES_SUMMARY.md` | `/theories/projects/tex/projet_uni_car_savard_01.tex` | `ref_generique` | 235 |
| `agent-multiloop-Gabriel-local\GABRIEL_COMPLETE_VISION_INTEGRATION.md` | `result.py` | `ref_generique` | 32 |
| `agent-multiloop-Gabriel-local\GABRIEL_COMPLETE_VISION_INTEGRATION.md` | `//github.com/UB-Mannheim/tesseract/wiki` | `ref_generique` | 113 |
| `agent-multiloop-Gabriel-local\GABRIEL_COMPLETE_VISION_INTEGRATION.md` | `pytesseract.pytesseract.py` | `ref_generique` | 117 |
| `agent-multiloop-Gabriel-local\GABRIEL_COMPLETE_VISION_INTEGRATION.md` | `/Gabriel/image_cache` | `ref_generique` | 128 |
| `agent-multiloop-Gabriel-local\GABRIEL_COMPLETE_VISION_INTEGRATION.md` | `/Users/Philippe/Desktop/triangle.png` | `ref_generique` | 137 |
| `agent-multiloop-Gabriel-local\GABRIEL_COMPLETE_VISION_INTEGRATION.md` | `//example.com/data_table.png` | `ref_generique` | 149 |
| `agent-multiloop-Gabriel-local\GABRIEL_COMPLETE_VISION_INTEGRATION.md` | `analysis.json` | `ref_generique` | 188 |
| `agent-multiloop-Gabriel-local\GABRIEL_COMPLETE_VISION_INTEGRATION.md` | `result.json` | `ref_generique` | 189 |
| `agent-multiloop-Gabriel-local\GABRIEL_FINAL_SOLUTION.txt` | `//localhost` | `ref_generique` | 46 |
| `agent-multiloop-Gabriel-local\GABRIEL_FINAL_v5_SOCKET_CLEANUP.md` | `/home/agent/app/` | `ref_generique` | 75 |
| `agent-multiloop-Gabriel-local\GABRIEL_FINAL_v5_SOCKET_CLEANUP.md` | `//localhost` | `ref_generique` | 89 |
| `agent-multiloop-Gabriel-local\GABRIEL_IMAGE_ANALYSIS_COMPLETE_GUIDE.md` | `//localhost` | `ref_generique` | 80 |
| `agent-multiloop-Gabriel-local\GABRIEL_IMAGE_ANALYSIS_COMPLETE_GUIDE.md` | `result.json` | `ref_generique` | 140 |
| `agent-multiloop-Gabriel-local\GABRIEL_IMAGE_ANALYSIS_COMPLETE_GUIDE.md` | `./data/cache/vision` | `ref_generique` | 345 |
| `agent-multiloop-Gabriel-local\gabriel_mathematical.py` | `config_mathematical.env` | `chemin_litteral` | 37 |
| `agent-multiloop-Gabriel-local\GABRIEL_PARAMETRIC_VALIDATION_GUIDE.md` | `/schema/beau_soleil.png` | `ref_generique` | 97 |
| `agent-multiloop-Gabriel-local\GABRIEL_PARAMETRIC_VALIDATION_GUIDE.md` | `/figures/mon_triangle.png` | `ref_generique` | 115 |
| `agent-multiloop-Gabriel-local\GABRIEL_PARAMETRIC_VALIDATION_GUIDE.md` | `/cercle.png` | `ref_generique` | 137 |
| `agent-multiloop-Gabriel-local\GABRIEL_PARAMETRIC_VALIDATION_GUIDE.md` | `/triangle.png` | `ref_generique` | 154 |
| `agent-multiloop-Gabriel-local\GABRIEL_PARAMETRIC_VALIDATION_GUIDE.md` | `/rectangle.png` | `ref_generique` | 173 |
| `agent-multiloop-Gabriel-local\GABRIEL_PARAMETRIC_VALIDATION_GUIDE.md` | `/path/image.png` | `ref_generique` | 251 |
| `agent-multiloop-Gabriel-local\GABRIEL_PARAMETRIC_VALIDATION_GUIDE.md` | `/schema/figure.png` | `ref_generique` | 338 |
| `agent-multiloop-Gabriel-local\GABRIEL_PORT_FIX_v5.3.md` | `//localhost` | `ref_generique` | 82 |
| `agent-multiloop-Gabriel-local\GABRIEL_v3.0_MULTILOOP_VALIDATION.md` | `théorie.thy` | `ref_generique` | 33 |
| `agent-multiloop-Gabriel-local\GABRIEL_v3.0_MULTILOOP_VALIDATION.md` | `results.json` | `ref_generique` | 164 |
| `agent-multiloop-Gabriel-local\GABRIEL_v4.0_THEORY_MEMORY.md` | `axioms.json` | `ref_generique` | 32 |
| `agent-multiloop-Gabriel-local\GABRIEL_v5.0_FINAL_SUMMARY.txt` | `//localhost` | `ref_generique` | 127 |
| `agent-multiloop-Gabriel-local\GABRIEL_v5.4_WORKING_SOLUTION.md` | `//localhost` | `ref_generique` | 60 |
| `agent-multiloop-Gabriel-local\GABRIEL_v5_EXPLIQUE_SIMPLEMENT.txt` | `//localhost` | `ref_generique` | 124 |
| `agent-multiloop-Gabriel-local\GABRIEL_v5_UPDATE_GUIDE.md` | `//localhost` | `ref_generique` | 82 |
| `agent-multiloop-Gabriel-local\GABRIEL_VALIDATION_EXAMPLES.md` | `/schema/beau_soleil.png` | `ref_generique` | 15 |
| `agent-multiloop-Gabriel-local\GABRIEL_VALIDATION_EXAMPLES.md` | `/figures/mon_triangle.png` | `ref_generique` | 45 |
| `agent-multiloop-Gabriel-local\GABRIEL_VALIDATION_EXAMPLES.md` | `/cercle.png` | `ref_generique` | 66 |
| `agent-multiloop-Gabriel-local\GABRIEL_VALIDATION_EXAMPLES.md` | `/triangle.png` | `ref_generique` | 108 |
| `agent-multiloop-Gabriel-local\GABRIEL_VALIDATION_EXAMPLES.md` | `/figure.png` | `ref_generique` | 147 |
| `agent-multiloop-Gabriel-local\GABRIEL_VALIDATION_EXAMPLES.md` | `/rectangle.png` | `ref_generique` | 176 |
| `agent-multiloop-Gabriel-local\GABRIEL_VALIDATION_EXAMPLES.md` | `/etoile.png` | `ref_generique` | 221 |
| `agent-multiloop-Gabriel-local\GABRIEL_VALIDATION_EXAMPLES.md` | `/soleil.png` | `ref_generique` | 257 |
| `agent-multiloop-Gabriel-local\GABRIEL_VALIDATION_EXAMPLES.md` | `/schema/complexe.png` | `ref_generique` | 327 |
| `agent-multiloop-Gabriel-local\GABRIEL_VALIDATION_EXAMPLES.md` | `/image.png` | `ref_generique` | 379 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` | `//serveur/partage/fichier.png` | `ref_generique` | 11 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` | `//example.com/image.png` | `ref_generique` | 12 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` | `/Users/Philippe/Pictures/geometrie.png` | `ref_generique` | 41 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` | `./data/figures/triangle.jpg` | `ref_generique` | 42 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` | `/home/user/images/schema.png` | `ref_generique` | 43 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` | `result.py` | `ref_generique` | 47 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` | `//example.com/my-figure.png` | `ref_generique` | 53 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` | `//192.168.1.100/shared/diagram.png` | `ref_generique` | 67 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` | `/path/to/triangle.png` | `ref_generique` | 81 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` | `/tmp/gabriel_image_cache` | `ref_generique` | 157 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` | `/MesDocuments/Figures` | `ref_generique` | 171 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` | `/mnt/shared/diagrams` | `ref_generique` | 172 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` | `/Users/Me/Desktop/triangle.png` | `ref_generique` | 223 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` | `/Users/Philippe/Figures/schema.png` | `ref_generique` | 308 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` | `triangle_param.py` | `ref_generique` | 356 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` | `triangle_formal.thy` | `ref_generique` | 360 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` | `result.sh` | `ref_generique` | 378 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_QUICK_START.md` | `./test_image.png` | `ref_generique` | 51 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_QUICK_START.md` | `/path/to/figure.png` | `ref_generique` | 58 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_QUICK_START.md` | `//example.com/chart.png` | `ref_generique` | 59 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_QUICK_START.md` | `./data/spreadsheet_screenshot.png` | `ref_generique` | 61 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_QUICK_START.md` | `./image_cache` | `ref_generique` | 111 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_QUICK_START.md` | `/Users/Philippe/Desktop/mon_schema.png` | `ref_generique` | 115 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_QUICK_START.md` | `result.py` | `ref_generique` | 129 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_QUICK_START.md` | `analysis.json` | `ref_generique` | 136 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_QUICK_START.md` | `result.json` | `ref_generique` | 137 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_QUICK_START.md` | `//github.com/UB-Mannheim/tesseract/wiki` | `ref_generique` | 159 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_VERIFICATION_COMPLETE.md` | `//example.com/image.png` | `ref_generique` | 29 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_VERIFICATION_COMPLETE.md` | `//serveur/partage/fichier.png` | `ref_generique` | 31 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_VERIFICATION_COMPLETE.md` | `/path/to/image.png` | `ref_generique` | 171 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_VERIFICATION_COMPLETE.md` | `result.py` | `ref_generique` | 180 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_VERIFICATION_COMPLETE.md` | `result.json` | `ref_generique` | 183 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_VERIFICATION_COMPLETE.md` | `/Desktop/triangle.png` | `ref_generique` | 188 |
| `agent-multiloop-Gabriel-local\GABRIEL_VISION_VERIFICATION_COMPLETE.md` | `//example.com/data.png` | `ref_generique` | 230 |
| `agent-multiloop-Gabriel-local\generate_thy_templates.py` | `{project_name}.thy` | `chemin_litteral` | 75 |
| `agent-multiloop-Gabriel-local\generate_thy_templates.py` | `  - projet_uni_car_savard_001.thy` | `chemin_litteral` | 101 |
| `agent-multiloop-Gabriel-local\generate_thy_templates.py` | `  - projet_uni_car_savard_002.thy` | `chemin_litteral` | 102 |
| `agent-multiloop-Gabriel-local\generate_thy_templates.py` | `  - projet_uni_car_savard_100.thy` | `chemin_litteral` | 104 |
| `agent-multiloop-Gabriel-local\generate_thy_templates.py` | `  - /theories/projects/projet_uni_car_savard_001.thy` | `chemin_litteral` | 109 |
| `agent-multiloop-Gabriel-local\generate_thy_templates.py` | `  - /theories/projects/projet_uni_car_savard_002.thy` | `chemin_litteral` | 110 |
| `agent-multiloop-Gabriel-local\generate_txt_tex_templates.py` | `{project_name}.txt` | `chemin_litteral` | 149 |
| `agent-multiloop-Gabriel-local\generate_txt_tex_templates.py` | `  ├── projet_uni_car_savard_*.thy` | `chemin_litteral` | 214 |
| `agent-multiloop-Gabriel-local\generate_txt_tex_templates.py` | `  ├── txt/projet_uni_car_savard_*.txt` | `chemin_litteral` | 215 |
| `agent-multiloop-Gabriel-local\GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md` | `spectral_matrix_n50.json` | `ref_generique` | 99 |
| `agent-multiloop-Gabriel-local\GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md` | `spectral_matrix_n50.py` | `ref_generique` | 101 |
| `agent-multiloop-Gabriel-local\GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md` | `./figures/quadrature.png` | `ref_generique` | 263 |
| `agent-multiloop-Gabriel-local\GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md` | `./figures/diagram.png` | `ref_generique` | 365 |
| `agent-multiloop-Gabriel-local\GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md` | `matplotlib.py` | `ref_generique` | 501 |
| `agent-multiloop-Gabriel-local\GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md` | `plt.sh` | `ref_generique` | 520 |
| `agent-multiloop-Gabriel-local\GUIDE_JEDIT_GABRIEL.md` | `theorem_proof.thy` | `ref_generique` | 10 |
| `agent-multiloop-Gabriel-local\GUIDE_JEDIT_GABRIEL.md` | `/theories/generated_` | `ref_generique` | 12 |
| `agent-multiloop-Gabriel-local\GUIDE_JEDIT_GABRIEL.md` | `//sourceforge.net/projects/vcxsrv/` | `ref_generique` | 42 |
| `agent-multiloop-Gabriel-local\GUIDE_JEDIT_GABRIEL.md` | `./theories:/theories` | `ref_generique` | 64 |
| `agent-multiloop-Gabriel-local\GUIDE_JEDIT_GABRIEL.md` | `/home/isabelle/.isabelle/heaps` | `ref_generique` | 65 |
| `agent-multiloop-Gabriel-local\GUIDE_JEDIT_GABRIEL.md` | `/tmp/.X11-unix` | `ref_generique` | 67 |
| `agent-multiloop-Gabriel-local\GUIDE_JEDIT_GABRIEL.md` | `/bin/bash` | `ref_generique` | 72 |
| `agent-multiloop-Gabriel-local\GUIDE_JEDIT_GABRIEL.md` | `/dev/null` | `ref_generique` | 73 |
| `agent-multiloop-Gabriel-local\GUIDE_JEDIT_GABRIEL.md` | `/theories/example.thy` | `ref_generique` | 89 |
| `agent-multiloop-Gabriel-local\GUIDE_JEDIT_GABRIEL.md` | `/theories/generated/` | `ref_generique` | 107 |
| `agent-multiloop-Gabriel-local\GUIDE_JEDIT_GABRIEL.md` | `/theories/generated_1234567890.thy` | `ref_generique` | 130 |
| `agent-multiloop-Gabriel-local\GUIDE_JEDIT_GABRIEL.md` | `/theories` | `ref_generique` | 238 |
| `agent-multiloop-Gabriel-local\GUIDE_JEDIT_GABRIEL.md` | `//localhost` | `ref_generique` | 273 |
| `agent-multiloop-Gabriel-local\GUIDE_JEDIT_GABRIEL.md` | `/query` | `ref_generique` | 291 |
| `agent-multiloop-Gabriel-local\GUIDE_JEDIT_GABRIEL.md` | `/theories/generated.thy` | `ref_generique` | 308 |
| `agent-multiloop-Gabriel-local\HOL4_SYSTEMATIC_PROOFS.md` | `riemann_spectral.thy` | `ref_generique` | 71 |
| `agent-multiloop-Gabriel-local\HOL4_SYSTEMATIC_PROOFS.md` | `result_proof.thy` | `ref_generique` | 193 |
| `agent-multiloop-Gabriel-local\HOL_ISABELLE_FIX.md` | `/theories` | `ref_generique` | 151 |
| `agent-multiloop-Gabriel-local\IMAGE_ANALYSIS_ANSWER_DIRECT.md` | `//localhost` | `ref_generique` | 230 |
| `agent-multiloop-Gabriel-local\INDEX.md` | `//localhost` | `ref_generique` | 146 |
| `agent-multiloop-Gabriel-local\integration_mathematical.py` | `/api/mathematical/query` | `chemin_litteral` | 103 |
| `agent-multiloop-Gabriel-local\integration_mathematical.py` | `/api/mathematical/capabilities` | `chemin_litteral` | 144 |
| `agent-multiloop-Gabriel-local\INTEGRATION_PATCH_IMAGE_ANALYSIS.md` | `/path/image.png` | `ref_generique` | 44 |
| `agent-multiloop-Gabriel-local\INTEGRATION_PATCH_IMAGE_ANALYSIS.md` | `/path/to/file.ext` | `ref_generique` | 124 |
| `agent-multiloop-Gabriel-local\INTEGRATION_PATCH_IMAGE_ANALYSIS.md` | `./path` | `ref_generique` | 130 |
| `agent-multiloop-Gabriel-local\INTEGRATION_UNIVERSESTAUCARRE.md` | `emergent.sh` | `ref_generique` | 8 |
| `agent-multiloop-Gabriel-local\INTEGRATION_UNIVERSESTAUCARRE.md` | `/sync/universestaucarre` | `ref_generique` | 11 |
| `agent-multiloop-Gabriel-local\INTEGRATION_UNIVERSESTAUCARRE.md` | `/query` | `ref_generique` | 18 |
| `agent-multiloop-Gabriel-local\INTEGRATION_UNIVERSESTAUCARRE.md` | `/isabelle/verify` | `ref_generique` | 20 |
| `agent-multiloop-Gabriel-local\INTEGRATION_UNIVERSESTAUCARRE.md` | `/health` | `ref_generique` | 21 |
| `agent-multiloop-Gabriel-local\INTEGRATION_UNIVERSESTAUCARRE.md` | `//localhost` | `ref_generique` | 50 |
| `agent-multiloop-Gabriel-local\INTEGRATION_UNIVERSESTAUCARRE.md` | `//0.0.0.0` | `ref_generique` | 53 |
| `agent-multiloop-Gabriel-local\INTEGRATION_UNIVERSESTAUCARRE.md` | `response.json` | `ref_generique` | 87 |
| `agent-multiloop-Gabriel-local\INTEGRATION_UNIVERSESTAUCARRE.md` | `//192.168.1.100` | `ref_generique` | 123 |
| `agent-multiloop-Gabriel-local\INTEGRATION_UNIVERSESTAUCARRE.md` | `//gabriel-local.home` | `ref_generique` | 125 |
| `agent-multiloop-Gabriel-local\INTEGRATION_UNIVERSESTAUCARRE.md` | `/home/agent/app/data/universestaucarre-sync/` | `ref_generique` | 245 |
| `agent-multiloop-Gabriel-local\INTEGRATION_UNIVERSESTAUCARRE.md` | `//gabriel` | `ref_generique` | 293 |
| `agent-multiloop-Gabriel-local\JEDIT_QUICK_REFERENCE.md` | `/theories/example.thy` | `ref_generique` | 15 |
| `agent-multiloop-Gabriel-local\JEDIT_QUICK_REFERENCE.md` | `/theories/file.thy` | `ref_generique` | 26 |
| `agent-multiloop-Gabriel-local\JEDIT_QUICK_REFERENCE.md` | `//localhost` | `ref_generique` | 65 |
| `agent-multiloop-Gabriel-local\JEDIT_QUICK_REFERENCE.md` | `/theories/generated_1234567890.thy` | `ref_generique` | 87 |
| `agent-multiloop-Gabriel-local\JEDIT_QUICK_REFERENCE.md` | `generated_1234567890.thy` | `ref_generique` | 94 |
| `agent-multiloop-Gabriel-local\JEDIT_QUICK_REFERENCE.md` | `//sourceforge.net/projects/vcxsrv/` | `ref_generique` | 157 |
| `agent-multiloop-Gabriel-local\JEDIT_QUICK_REFERENCE.md` | `/theories/generated/` | `ref_generique` | 218 |
| `agent-multiloop-Gabriel-local\JEDIT_QUICK_REFERENCE.md` | `//0.0.0.0` | `ref_generique` | 225 |
| `agent-multiloop-Gabriel-local\JEDIT_QUICK_REFERENCE.md` | `/theories` | `ref_generique` | 263 |
| `agent-multiloop-Gabriel-local\memory\methode_spectral_section_XI.py` | `methode_spectral_section_XI.thy` | `chemin_litteral` | 84 |
| `agent-multiloop-Gabriel-local\MIGRATION_VALIDATION_SYSTEMS.md` | `/schema/beau_soleil.png` | `ref_generique` | 9 |
| `agent-multiloop-Gabriel-local\MIGRATION_VALIDATION_SYSTEMS.md` | `/schema/soleil.png` | `ref_generique` | 66 |
| `agent-multiloop-Gabriel-local\MULTIFORMAT_TEMPLATES_GUIDE.md` | `/theories/projects/projet_uni_car_savard_26.thy` | `ref_generique` | 169 |
| `agent-multiloop-Gabriel-local\MULTIFORMAT_TEMPLATES_GUIDE.md` | `/theories/projects/txt/projet_uni_car_savard_26.txt` | `ref_generique` | 174 |
| `agent-multiloop-Gabriel-local\MULTIFORMAT_TEMPLATES_GUIDE.md` | `/theories/projects/tex/projet_uni_car_savard_26.tex` | `ref_generique` | 178 |
| `agent-multiloop-Gabriel-local\MULTIFORMAT_TEMPLATES_GUIDE.md` | `/theories/projects/` | `ref_generique` | 199 |
| `agent-multiloop-Gabriel-local\MULTIFORMAT_TEMPLATES_GUIDE.md` | `/theories/projects/txt/` | `ref_generique` | 200 |
| `agent-multiloop-Gabriel-local\MULTIFORMAT_TEMPLATES_GUIDE.md` | `/theories/projects/tex/` | `ref_generique` | 201 |
| `agent-multiloop-Gabriel-local\MULTIFORMAT_TEMPLATES_GUIDE.md` | `/theories/projects/txt/projet_uni_car_savard_42.txt` | `ref_generique` | 204 |
| `agent-multiloop-Gabriel-local\MULTIFORMAT_TEMPLATES_GUIDE.md` | `/theories/projects` | `ref_generique` | 220 |
| `agent-multiloop-Gabriel-local\MULTIFORMAT_TEMPLATES_GUIDE.md` | `self.thy` | `ref_generique` | 222 |
| `agent-multiloop-Gabriel-local\MULTIFORMAT_TEMPLATES_GUIDE.md` | `self.txt` | `ref_generique` | 223 |
| `agent-multiloop-Gabriel-local\MULTIFORMAT_TEMPLATES_GUIDE.md` | `./theories:/theories` | `ref_generique` | 284 |
| `agent-multiloop-Gabriel-local\MULTIFORMAT_TEMPLATES_GUIDE.md` | `/theories/projects/projet_uni_car_savard_42.thy` | `ref_generique` | 304 |
| `agent-multiloop-Gabriel-local\MULTIFORMAT_TEMPLATES_GUIDE.md` | `/theories/projects/tex/projet_uni_car_savard_42.tex` | `ref_generique` | 306 |
| `agent-multiloop-Gabriel-local\MULTIFORMAT_TEMPLATES_GUIDE.md` | `/theories/projects/tex` | `ref_generique` | 309 |
| `agent-multiloop-Gabriel-local\PATCH_IMAGE_ANALYSIS_INTEGRATION.py` | `/api/v1/image/analyze` | `chemin_litteral` | 87 |
| `agent-multiloop-Gabriel-local\PATCH_IMAGE_ANALYSIS_INTEGRATION.py` | `1. Ouvrir src/ui/cli.py` | `chemin_litteral` | 126 |
| `agent-multiloop-Gabriel-local\PORT_CLEANUP_IMPLEMENTATION.md` | `./gabriel_launcher.py:/home/agent/app/gabriel_launcher.py` | `ref_generique` | 43 |
| `agent-multiloop-Gabriel-local\PORT_CLEANUP_IMPLEMENTATION.md` | `./port_cleanup.py:/home/agent/app/port_cleanup.py` | `ref_generique` | 44 |
| `agent-multiloop-Gabriel-local\PORT_CLEANUP_IMPLEMENTATION.md` | `./theories:/home/agent/app/theories` | `ref_generique` | 82 |
| `agent-multiloop-Gabriel-local\PORT_CLEANUP_IMPLEMENTATION.md` | `/home/agent/app/theories/tex/` | `ref_generique` | 87 |
| `agent-multiloop-Gabriel-local\PORT_CLEANUP_IMPLEMENTATION.md` | `/home/agent/app/theories/tex/Geometrie_du_Spectre_des_Nombres_Premiers_2026.pdf` | `ref_generique` | 98 |
| `agent-multiloop-Gabriel-local\PORT_CLEANUP_IMPLEMENTATION.md` | `/theories/tex/` | `ref_generique` | 269 |
| `agent-multiloop-Gabriel-local\POWERSHELL_ISE_GUIDE.md` | `//localhost` | `ref_generique` | 29 |
| `agent-multiloop-Gabriel-local\PROJECTS_TEMPLATES_GUIDE.md` | `/theories/projects/projet_uni_car_savard_` | `ref_generique` | 29 |
| `agent-multiloop-Gabriel-local\PROJECTS_TEMPLATES_GUIDE.md` | `/generated/` | `ref_generique` | 41 |
| `agent-multiloop-Gabriel-local\PROJECTS_TEMPLATES_GUIDE.md` | `/theories/generated/projet_uni_car_savard_` | `ref_generique` | 42 |
| `agent-multiloop-Gabriel-local\PROJECTS_TEMPLATES_GUIDE.md` | `/theories/projects/` | `ref_generique` | 104 |
| `agent-multiloop-Gabriel-local\PROJECTS_TEMPLATES_GUIDE.md` | `/theories/projects/projet_uni_car_savard_42.thy` | `ref_generique` | 111 |
| `agent-multiloop-Gabriel-local\PROJECTS_TEMPLATES_GUIDE.md` | `/theories/projects/projet_uni_car_savard_15.thy` | `ref_generique` | 139 |
| `agent-multiloop-Gabriel-local\PROJECTS_TEMPLATES_GUIDE.md` | `/theories/archives/completed_15.thy` | `ref_generique` | 163 |
| `agent-multiloop-Gabriel-local\PROJECTS_TEMPLATES_GUIDE.md` | `/theories/projects` | `ref_generique` | 181 |
| `agent-multiloop-Gabriel-local\PROJECTS_TEMPLATES_GUIDE.md` | `/theories/generated/` | `ref_generique` | 232 |
| `agent-multiloop-Gabriel-local\PROJECTS_TEMPLATES_GUIDE.md` | `execution_projet_01.thy` | `ref_generique` | 248 |
| `agent-multiloop-Gabriel-local\PROJECTS_TEMPLATES_GUIDE.md` | `execution_projet_02.thy` | `ref_generique` | 249 |
| `agent-multiloop-Gabriel-local\PROJECTS_TEMPLATES_GUIDE.md` | `completed_01.thy` | `ref_generique` | 253 |
| `agent-multiloop-Gabriel-local\PROJECTS_TEMPLATES_GUIDE.md` | `./theories:/theories` | `ref_generique` | 266 |
| `agent-multiloop-Gabriel-local\PROJECTS_TEMPLATES_GUIDE.md` | `./theories:/home/agent/app/theories:ro` | `ref_generique` | 267 |
| `agent-multiloop-Gabriel-local\PROJECTS_TEMPLATES_GUIDE.md` | `/theories/projects/projet_uni_car_savard_01.thy` | `ref_generique` | 303 |
| `agent-multiloop-Gabriel-local\PYTEST_CHECKLIST.md` | `/home/agent/app` | `ref_generique` | 29 |
| `agent-multiloop-Gabriel-local\PYTEST_CHECKLIST.md` | `rapport_tests.txt` | `ref_generique` | 149 |
| `agent-multiloop-Gabriel-local\PYTEST_EXECUTION_GUIDE.md` | `/home/agent/app` | `ref_generique` | 53 |
| `agent-multiloop-Gabriel-local\PYTEST_INDEX.md` | `/home/agent/app` | `ref_generique` | 88 |
| `agent-multiloop-Gabriel-local\PYTEST_LIST_COMPLETE.md` | `/home/agent/app` | `ref_generique` | 156 |
| `agent-multiloop-Gabriel-local\PYTEST_SUMMARY.md` | `/home/agent/app` | `ref_generique` | 156 |
| `agent-multiloop-Gabriel-local\quick-start.sh` | `Please` | `shell_appel` | 21 |
| `agent-multiloop-Gabriel-local\quick-start.sh` | `Trying` | `shell_appel` | 25 |
| `agent-multiloop-Gabriel-local\QUICK_REFERENCE.md` | `//localhost` | `ref_generique` | 52 |
| `agent-multiloop-Gabriel-local\QUICK_START_IMAGE_ANALYSIS.md` | `//localhost` | `ref_generique` | 16 |
| `agent-multiloop-Gabriel-local\quick_verification.py` | `config_mathematical.env` | `chemin_litteral` | 51 |
| `agent-multiloop-Gabriel-local\quick_verification.py` | `theories/riemann_spectral.thy` | `chemin_litteral` | 53 |
| `agent-multiloop-Gabriel-local\quick_verification.py` | `README_MATHEMATICAL_v2.md` | `chemin_litteral` | 55 |
| `agent-multiloop-Gabriel-local\quick_verification.py` | `  1. pip install -r requirements.txt` | `chemin_litteral` | 173 |
| `agent-multiloop-Gabriel-local\quick_verification.py` | `\n[INFO] Consulter: SETUP_MATHEMATICAL_v2.md` | `chemin_litteral` | 187 |
| `agent-multiloop-Gabriel-local\RAPPORT_ANALYSE_DEPENDANCES.md` | `README_FINAL.md` | `ref_generique` | 146 |
| `agent-multiloop-Gabriel-local\RAPPORT_ETAPE1_ANALYSE_README.md` | `README_FINAL.md` | `ref_generique` | 10 |
| `agent-multiloop-Gabriel-local\RAPPORT_ETAPE1_ANALYSE_README.md` | `README_MATHEMATICAL_v2.md` | `ref_generique` | 11 |
| `agent-multiloop-Gabriel-local\RAPPORT_ETAPE1_ANALYSE_README.md` | `README_FOR_USER.txt` | `ref_generique` | 13 |
| `agent-multiloop-Gabriel-local\RAPPORT_ETAPE1_ANALYSE_README.md` | `README_v4.0.md` | `ref_generique` | 14 |
| `agent-multiloop-Gabriel-local\RAPPORT_MAINTENANCE_ETAPE3.md` | `README_FINAL.md` | `ref_generique` | 77 |
| `agent-multiloop-Gabriel-local\RAPPORT_MAINTENANCE_ETAPE3.md` | `README_MATHEMATICAL_v2.md` | `ref_generique` | 79 |
| `agent-multiloop-Gabriel-local\RAPPORT_MAINTENANCE_ETAPE3.md` | `README_FOR_USER.txt` | `ref_generique` | 81 |
| `agent-multiloop-Gabriel-local\RAPPORT_MAINTENANCE_ETAPE3.md` | `README_v4.0.md` | `ref_generique` | 82 |
| `agent-multiloop-Gabriel-local\README.md` | `//www.universestaucarre.com` | `ref_generique` | 31 |
| `agent-multiloop-Gabriel-local\README.md` | `//github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026.git` | `ref_generique` | 38 |
| `agent-multiloop-Gabriel-local\README.md` | `Emergent.sh` | `ref_generique` | 38 |
| `agent-multiloop-Gabriel-local\README.md` | `//localhost` | `ref_generique` | 251 |
| `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` | `//localhost` | `ref_generique` | 36 |
| `agent-multiloop-Gabriel-local\RELEASE_NOTES_v2.1.md` | `README_FINAL.md` | `ref_generique` | 43 |
| `agent-multiloop-Gabriel-local\RELEASE_NOTES_v2.1.md` | `README_MATHEMATICAL_v2.md` | `ref_generique` | 43 |
| `agent-multiloop-Gabriel-local\RELEASE_NOTES_v2.1.md` | `README_FOR_USER.txt` | `ref_generique` | 43 |
| `agent-multiloop-Gabriel-local\RELEASE_NOTES_v2.1.md` | `README_v4.0.md` | `ref_generique` | 43 |
| `agent-multiloop-Gabriel-local\RELEASE_NOTES_v2.1.md` | `//localhost` | `ref_generique` | 95 |
| `agent-multiloop-Gabriel-local\RELEASE_v2.1_COMPLETE.txt` | `README_FINAL.md` | `ref_generique` | 93 |
| `agent-multiloop-Gabriel-local\RELEASE_v2.1_COMPLETE.txt` | `README_MATHEMATICAL_v2.md` | `ref_generique` | 94 |
| `agent-multiloop-Gabriel-local\RELEASE_v2.1_COMPLETE.txt` | `README_FOR_USER.txt` | `ref_generique` | 95 |
| `agent-multiloop-Gabriel-local\RELEASE_v2.1_COMPLETE.txt` | `README_v4.0.md` | `ref_generique` | 96 |
| `agent-multiloop-Gabriel-local\RELEASE_v2.1_COMPLETE.txt` | `setup.py` | `ref_generique` | 226 |
| `agent-multiloop-Gabriel-local\requirements.txt` | `SETUP.md` | `ref_generique` | 55 |
| `agent-multiloop-Gabriel-local\RESUME_SESSION_COMPLETE.md` | `advanced_analysis_criteria_v2.py` | `ref_generique` | 94 |
| `agent-multiloop-Gabriel-local\scripts\healthcheck_tex.sh` | `-` | `shell_appel` | 3 |
| `agent-multiloop-Gabriel-local\scripts\healthcheck_tex.sh` | `path/to/file.tex` | `shell_appel` | 18 |
| `agent-multiloop-Gabriel-local\scripts\healthcheck_tex.sh` | `.git/hooks/pre-commit` | `shell_appel` | 21 |
| `agent-multiloop-Gabriel-local\scripts\healthcheck_tex.sh` | `if` | `shell_appel` | 35 |
| `agent-multiloop-Gabriel-local\scripts\healthcheck_tex.sh` | `def` | `shell_appel` | 82 |
| `agent-multiloop-Gabriel-local\scripts\healthcheck_tex.sh` | `starred_secs` | `shell_appel` | 104 |
| `agent-multiloop-Gabriel-local\scripts\healthcheck_tex.sh` | `Compilation` | `shell_appel` | 156 |
| `agent-multiloop-Gabriel-local\scripts\isabelle-integration.sh` | `Surveille` | `shell_appel` | 7 |
| `agent-multiloop-Gabriel-local\scripts\isabelle-integration.sh` | `Traite` | `shell_appel` | 8 |
| `agent-multiloop-Gabriel-local\scripts\isabelle-integration.sh` | `Envoie` | `shell_appel` | 9 |
| `agent-multiloop-Gabriel-local\scripts\isabelle-integration.sh` | `Sauvegarde` | `shell_appel` | 10 |
| `agent-multiloop-Gabriel-local\scripts\isabelle_static_check.py` | `theories/methode_spectral.thy` | `chemin_litteral` | 21 |
| `agent-multiloop-Gabriel-local\scripts\translate_thy.py` | `theories/methode_spectral.thy` | `Path()` | 32 |
| `agent-multiloop-Gabriel-local\scripts\translate_thy.py` | `theories` | `Path()` | 33 |
| `agent-multiloop-Gabriel-local\scripts\translate_thy.py` | `methode_spectral_{lang_code}.thy` | `chemin_litteral` | 519 |
| `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` | `riemann_spectral.thy` | `ref_generique` | 20 |
| `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` | `pdf_index.json` | `ref_generique` | 26 |
| `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` | `config_mathematical.env` | `ref_generique` | 28 |
| `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` | `//github.com/HOL-Theorem-Prover/HOL` | `ref_generique` | 51 |
| `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` | `//raw.githubusercontent.com/leanprover/elan/master/elan-init.sh` | `ref_generique` | 75 |
| `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` | `//www.wolfram.com/engine/free-license/` | `ref_generique` | 105 |
| `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` | `/usr/bin/holmake` | `ref_generique` | 119 |
| `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` | `/home/user/.elan/toolchains/leanprover--lean4---v4.0.0/bin` | `ref_generique` | 123 |
| `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` | `/c/Users/user/.elan/toolchains/leanprover--lean4---v4.0.0/bin` | `ref_generique` | 124 |
| `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` | `/opt/Wolfram/WolframKernel` | `ref_generique` | 131 |
| `agent-multiloop-Gabriel-local\SHORTCUTS_AND_TIPS.md` | `//localhost` | `ref_generique` | 79 |
| `agent-multiloop-Gabriel-local\SOLUTION_SUMMARY_v5.3.txt` | `//localhost` | `ref_generique` | 27 |
| `agent-multiloop-Gabriel-local\SOLUTION_SUMMARY_v5.3.txt` | `/home/agent/app/theories/tex/` | `ref_generique` | 123 |
| `agent-multiloop-Gabriel-local\src\adapters\corpus\certainty_kernel.py` | `/home/agent/app/theories` | `chemin_litteral` | 62 |
| `agent-multiloop-Gabriel-local\src\adapters\corpus\thy_loader.py` | `/theories` | `chemin_litteral` | 22 |
| `agent-multiloop-Gabriel-local\src\adapters\corpus\thy_loader.py` | `*.thy` | `chemin_litteral` | 30 |
| `agent-multiloop-Gabriel-local\src\adapters\gabriel_isabelle_bridge.py` | `/theories` | `chemin_litteral` | 29 |
| `agent-multiloop-Gabriel-local\src\adapters\gabriel_isabelle_bridge.py` | `gabriel_{timestamp}.thy` | `chemin_litteral` | 53 |
| `agent-multiloop-Gabriel-local\src\adapters\gabriel_multiformat_manager.py` | `/home/agent/app/theories/projects` | `chemin_litteral` | 19 |
| `agent-multiloop-Gabriel-local\src\adapters\gabriel_multiformat_manager.py` | `projet_uni_car_savard_{i:02d}.thy` | `chemin_litteral` | 32 |
| `agent-multiloop-Gabriel-local\src\adapters\gabriel_multiformat_manager.py` | `projet_uni_car_savard_{i:02d}.txt` | `chemin_litteral` | 33 |
| `agent-multiloop-Gabriel-local\src\adapters\gabriel_multiformat_manager.py` | `projet_uni_car_savard_{project_num:02d}.thy` | `chemin_litteral` | 52 |
| `agent-multiloop-Gabriel-local\src\adapters\gabriel_multiformat_manager.py` | `projet_uni_car_savard_{project_num:02d}.txt` | `chemin_litteral` | 53 |
| `agent-multiloop-Gabriel-local\src\adapters\gabriel_project_manager.py` | `/home/agent/app/theories/projects` | `chemin_litteral` | 17 |
| `agent-multiloop-Gabriel-local\src\adapters\gabriel_project_manager.py` | `projet_uni_car_savard_*.thy` | `chemin_litteral` | 24 |
| `agent-multiloop-Gabriel-local\src\adapters\gabriel_project_manager.py` | `projet_uni_car_savard_{project_num:02d}.thy` | `chemin_litteral` | 44 |
| `agent-multiloop-Gabriel-local\src\adapters\gabriel_project_manager.py` | `execution_projet_{template_num:02d}.thy` | `chemin_litteral` | 105 |
| `agent-multiloop-Gabriel-local\src\adapters\hol_isabelle\isabelle_adapter.py` | `/opt/Isabelle2025-2` | `chemin_litteral` | 28 |
| `agent-multiloop-Gabriel-local\src\adapters\hol_isabelle\isabelle_adapter.py` | `/theories` | `chemin_litteral` | 30 |
| `agent-multiloop-Gabriel-local\src\adapters\hol_isabelle\isabelle_adapter.py` | `{theory_name}.thy` | `chemin_litteral` | 115 |
| `agent-multiloop-Gabriel-local\src\adapters\wolfram\wolfram_client.py` | `WOLFRAM_APP_ID absent ou non configure dans .env` | `chemin_litteral` | 63 |
| `agent-multiloop-Gabriel-local\src\api\gabriel_http_api.py` | `/home/agent/app/data/isabelle-results` | `Path()` | 118 |
| `agent-multiloop-Gabriel-local\src\api\gabriel_http_api.py` | `/home/agent/app/data/universestaucarre-sync` | `Path()` | 199 |
| `agent-multiloop-Gabriel-local\src\api\gabriel_http_api.py` | `/api/*` | `chemin_litteral` | 31 |
| `agent-multiloop-Gabriel-local\src\api\gabriel_http_api.py` | `/query` | `chemin_litteral` | 32 |
| `agent-multiloop-Gabriel-local\src\api\gabriel_http_api.py` | `/isabelle/*` | `chemin_litteral` | 33 |
| `agent-multiloop-Gabriel-local\src\api\gabriel_http_api.py` | `/sync/*` | `chemin_litteral` | 34 |
| `agent-multiloop-Gabriel-local\src\api\gabriel_http_api.py` | `/isabelle/verify` | `chemin_litteral` | 95 |
| `agent-multiloop-Gabriel-local\src\api\gabriel_http_api.py` | `/theories/example.thy` | `chemin_litteral` | 100 |
| `agent-multiloop-Gabriel-local\src\api\gabriel_http_api.py` | `)}.json` | `chemin_litteral` | 121 |
| `agent-multiloop-Gabriel-local\src\api\gabriel_http_api.py` | `/health` | `chemin_litteral` | 145 |
| `agent-multiloop-Gabriel-local\src\api\gabriel_http_api.py` | `/sync/universestaucarre` | `chemin_litteral` | 159 |
| `agent-multiloop-Gabriel-local\src\api\gabriel_http_api.py` | `sync_{session_id}.json` | `chemin_litteral` | 202 |
| `agent-multiloop-Gabriel-local\src\api\gabriel_http_api.py` | `/stream` | `chemin_litteral` | 241 |
| `agent-multiloop-Gabriel-local\src\audit\audit_store.py` | `/home/agent/app/data/audits` | `chemin_litteral` | 107 |
| `agent-multiloop-Gabriel-local\src\audit\audit_store.py` | `)}_{record.id}.json` | `chemin_litteral` | 175 |
| `agent-multiloop-Gabriel-local\src\audit\audit_store.py` | `*_{record_id}.json` | `chemin_litteral` | 190 |
| `agent-multiloop-Gabriel-local\src\audit\audit_store.py` | `*.json` | `chemin_litteral` | 213 |
| `agent-multiloop-Gabriel-local\src\cognitive\engine_bridge.py` | `data/learning` | `Path()` | 34 |
| `agent-multiloop-Gabriel-local\src\cognitive\engine_bridge.py` | `stats.json` | `chemin_litteral` | 44 |
| `agent-multiloop-Gabriel-local\src\cognitive\meta_reasoning.py` | `a` | `open_fichier` | 142 |
| `agent-multiloop-Gabriel-local\src\cognitive\meta_reasoning.py` | `data/learning/stats.json` | `chemin_litteral` | 64 |
| `agent-multiloop-Gabriel-local\src\core\config.py` | `/home/agent/app/.env` | `Path()` | 30 |
| `agent-multiloop-Gabriel-local\src\core\config.py` | `/home/agent/app/config.yaml` | `Path()` | 74 |
| `agent-multiloop-Gabriel-local\src\core\config.py` | `env_file: - .env` | `chemin_litteral` | 59 |
| `agent-multiloop-Gabriel-local\src\core\config.py` | `/theories` | `chemin_litteral` | 127 |
| `agent-multiloop-Gabriel-local\src\core\filesystem_access.py` | `/home/agent/app/theorie-savard` | `chemin_litteral` | 121 |
| `agent-multiloop-Gabriel-local\src\core\filesystem_access.py` | `/home/agent/app/data/theorie-savard` | `chemin_litteral` | 122 |
| `agent-multiloop-Gabriel-local\src\core\filesystem_access.py` | `/workspace/theorie-savard` | `chemin_litteral` | 123 |
| `agent-multiloop-Gabriel-local\src\core\logging_setup.py` | `./logs` | `chemin_litteral` | 26 |
| `agent-multiloop-Gabriel-local\src\core\pipeline.py` | `/theories` | `chemin_litteral` | 84 |
| `agent-multiloop-Gabriel-local\src\core\pipeline.py` | `/home/agent/app/data/audits` | `chemin_litteral` | 109 |
| `agent-multiloop-Gabriel-local\src\core\pipeline_with_gap_detection.py` | `data/graphs` | `Path()` | 251 |
| `agent-multiloop-Gabriel-local\src\engines\question_graphs.py` | `data/graphs` | `Path()` | 17 |
| `agent-multiloop-Gabriel-local\src\gabriel_vision_integration.py` | `/[^\s` | `chemin_litteral` | 89 |
| `agent-multiloop-Gabriel-local\src\hol_lean_interface.py` | `/theories` | `chemin_litteral` | 34 |
| `agent-multiloop-Gabriel-local\src\hol_lean_interface.py` | `/lean` | `chemin_litteral` | 155 |
| `agent-multiloop-Gabriel-local\src\image_access_manager.py` | `/tmp` | `Path()` | 85 |
| `agent-multiloop-Gabriel-local\src\image_access_manager.py` | `./images/graphique.jpg` | `chemin_litteral` | 487 |
| `agent-multiloop-Gabriel-local\src\image_access_manager.py` | `./images/figure.jpg` | `chemin_litteral` | 520 |
| `agent-multiloop-Gabriel-local\src\image_discovery_system.py` | `./data/image_index` | `Path()` | 57 |
| `agent-multiloop-Gabriel-local\src\image_discovery_system.py` | `/home` | `Path()` | 184 |
| `agent-multiloop-Gabriel-local\src\image_discovery_system.py` | `C:/theories` | `Path()` | 193 |
| `agent-multiloop-Gabriel-local\src\image_discovery_system.py` | `./figures` | `Path()` | 194 |
| `agent-multiloop-Gabriel-local\src\image_discovery_system.py` | `./images` | `Path()` | 195 |
| `agent-multiloop-Gabriel-local\src\image_discovery_system.py` | `./data` | `Path()` | 196 |
| `agent-multiloop-Gabriel-local\src\image_discovery_system.py` | `image_index.json` | `chemin_litteral` | 61 |
| `agent-multiloop-Gabriel-local\src\isabelle_validator.py` | `/usr/bin/isabelle` | `chemin_litteral` | 77 |
| `agent-multiloop-Gabriel-local\src\isabelle_validator.py` | `/opt/isabelle/bin/isabelle` | `chemin_litteral` | 78 |
| `agent-multiloop-Gabriel-local\src\isabelle_validator.py` | `/Applications/Isabelle.app/Isabelle` | `chemin_litteral` | 80 |
| `agent-multiloop-Gabriel-local\src\isabelle_validator.py` | `Exécute Isabelle sur fichier .thy` | `chemin_litteral` | 200 |
| `agent-multiloop-Gabriel-local\src\learning\debugging_expertise.py` | `/home/agent/app/data/expertise` | `Path()` | 159 |
| `agent-multiloop-Gabriel-local\src\learning\debugging_expertise.py` | `{record.session_id}.json` | `chemin_litteral` | 267 |
| `agent-multiloop-Gabriel-local\src\learning\debugging_expertise.py` | `*.json` | `chemin_litteral` | 274 |
| `agent-multiloop-Gabriel-local\src\mathematical_engine.py` | `Reference riemann_hypothesis_spectral.thy` | `chemin_litteral` | 141 |
| `agent-multiloop-Gabriel-local\src\mathematical_engine.py` | `gap_distribution lemma in riemann_spectral.thy` | `chemin_litteral` | 181 |
| `agent-multiloop-Gabriel-local\src\mathematical_engine.py` | `prime_decomposition in number_theory.thy` | `chemin_litteral` | 203 |
| `agent-multiloop-Gabriel-local\src\mathematical_engine.py` | `prime_number_theorem in analytic_number_theory.thy` | `chemin_litteral` | 237 |
| `agent-multiloop-Gabriel-local\src\multiloop\debat_orchestrator.py` | `data/debats` | `Path()` | 95 |
| `agent-multiloop-Gabriel-local\src\multiloop\debat_orchestrator.py` | `{stem}.json` | `chemin_litteral` | 522 |
| `agent-multiloop-Gabriel-local\src\multiloop\debat_orchestrator.py` | `{stem}.md` | `chemin_litteral` | 531 |
| `agent-multiloop-Gabriel-local\src\multiloop\gabriel_domain_config.py` | `chaos_harmonic_discrete.thy` | `chemin_litteral` | 49 |
| `agent-multiloop-Gabriel-local\src\multiloop\gabriel_domain_config.py` | `univers_carre_postulat.thy` | `chemin_litteral` | 54 |
| `agent-multiloop-Gabriel-local\src\multiloop\gabriel_domain_config.py` | `espace_philippot.thy` | `chemin_litteral` | 59 |
| `agent-multiloop-Gabriel-local\src\multiloop\gabriel_domain_config.py` | `Requête technique HOL/Isabelle sur methode_spectral.thy` | `chemin_litteral` | 69 |
| `agent-multiloop-Gabriel-local\src\multiloop\pre_reasoner.py` | `/rapide` | `chemin_litteral` | 391 |
| `agent-multiloop-Gabriel-local\src\multiloop\pre_reasoner.py` | `/standard` | `chemin_litteral` | 392 |
| `agent-multiloop-Gabriel-local\src\multiloop\pre_reasoner.py` | `/approfondi` | `chemin_litteral` | 393 |
| `agent-multiloop-Gabriel-local\src\multiloop\pre_reasoner.py` | `/complet` | `chemin_litteral` | 394 |
| `agent-multiloop-Gabriel-local\src\multiloop\pre_reasoner.py` | `/tres_complexe` | `chemin_litteral` | 395 |
| `agent-multiloop-Gabriel-local\src\multiloop\pre_reasoner.py` | `/instantane` | `chemin_litteral` | 396 |
| `agent-multiloop-Gabriel-local\src\pdf_rag_processor.py` | `/Title` | `chemin_litteral` | 74 |
| `agent-multiloop-Gabriel-local\src\pdf_rag_processor.py` | `/Author` | `chemin_litteral` | 75 |
| `agent-multiloop-Gabriel-local\src\pdf_rag_processor.py` | `/CreationDate` | `chemin_litteral` | 76 |
| `agent-multiloop-Gabriel-local\src\spectral\spectral_models.py` | `/ (sum_B(A_pos) - sum_B(B_pos))` | `chemin_litteral` | 175 |
| `agent-multiloop-Gabriel-local\src\ui\ask_gabriel.py` | `    - methode_spectral.thy` | `chemin_litteral` | 189 |
| `agent-multiloop-Gabriel-local\src\ui\ask_gabriel.py` | `    - geometrie_spectre_premier.thy` | `chemin_litteral` | 190 |
| `agent-multiloop-Gabriel-local\src\ui\ask_gabriel.py` | `    - riemann_spectral.thy` | `chemin_litteral` | 191 |
| `agent-multiloop-Gabriel-local\src\ui\ask_gabriel.py` | `     -> Verifiez que les valeurs attendues correspondent a .thy` | `chemin_litteral` | 295 |
| `agent-multiloop-Gabriel-local\src\ui\ci_status.py` | `/app/tests` | `chemin_litteral` | 76 |
| `agent-multiloop-Gabriel-local\src\ui\ci_status.py` | `/home/agent/app/tests` | `chemin_litteral` | 76 |
| `agent-multiloop-Gabriel-local\src\ui\ci_status.py` | `/workspace/tests` | `chemin_litteral` | 76 |
| `agent-multiloop-Gabriel-local\src\ui\cli.py` | `theories/projects` | `Path()` | 627 |
| `agent-multiloop-Gabriel-local\src\ui\cli.py` | `data/graphs` | `Path()` | 1611 |
| `agent-multiloop-Gabriel-local\src\ui\cli.py` | `/app/agent-multiloop-Gabriel-local` | `Path()` | 2091 |
| `agent-multiloop-Gabriel-local\src\ui\cli.py` | `/app` | `Path()` | 2092 |
| `agent-multiloop-Gabriel-local\src\ui\cli.py` | `1000 premiers indexes  -  Sections I a XII de methode_spectral.thy` | `chemin_litteral` | 213 |
| `agent-multiloop-Gabriel-local\src\validation_hol_knowledge.py` | `Représente un théorème du fichier validation_hol_unifiee.thy` | `chemin_litteral` | 21 |
| `agent-multiloop-Gabriel-local\src\visualization\__init__.py` | `data/graphs` | `Path()` | 15 |
| `agent-multiloop-Gabriel-local\START_HERE.txt` | `//localhost` | `ref_generique` | 17 |
| `agent-multiloop-Gabriel-local\START_HERE.txt` | `/home/agent/app/theories/tex/Geometrie_du_Spectre_des_Nombres_Premiers_2026.pdf` | `ref_generique` | 141 |
| `agent-multiloop-Gabriel-local\START_v5.0.txt` | `//localhost` | `ref_generique` | 85 |
| `agent-multiloop-Gabriel-local\SYNTHESE_RSA_v2.2.md` | `spectral_ratio_analyzer.py` | `ref_generique` | 58 |
| `agent-multiloop-Gabriel-local\SYNTHESE_ULTIME_v2.1.md` | `hol_proof_generator.py` | `ref_generique` | 15 |
| `agent-multiloop-Gabriel-local\SYNTHESE_ULTIME_v2.1.md` | `config_mathematical.env` | `ref_generique` | 34 |
| `agent-multiloop-Gabriel-local\SYNTHESE_ULTIME_v2.1.md` | `riemann_spectral.thy` | `ref_generique` | 197 |
| `agent-multiloop-Gabriel-local\TEMPLATES_SUMMARY.md` | `./theories:/theories` | `ref_generique` | 25 |
| `agent-multiloop-Gabriel-local\TEMPLATES_SUMMARY.md` | `/theories/projects/projet_uni_car_savard_` | `ref_generique` | 30 |
| `agent-multiloop-Gabriel-local\TEMPLATES_SUMMARY.md` | `project_uni_car_savard_42.thy` | `ref_generique` | 112 |
| `agent-multiloop-Gabriel-local\TEMPLATES_SUMMARY.md` | `/theories/generated/execution_projet_42.thy` | `ref_generique` | 117 |
| `agent-multiloop-Gabriel-local\TEMPLATES_SUMMARY.md` | `/theories/projects/projet_uni_car_savard_42.thy` | `ref_generique` | 179 |
| `agent-multiloop-Gabriel-local\TEMPLATES_SUMMARY.md` | `/theories/projects/` | `ref_generique` | 212 |
| `agent-multiloop-Gabriel-local\TEMPLATES_SUMMARY.md` | `/theories/projects/projet_uni_car_savard_01.thy` | `ref_generique` | 219 |
| `agent-multiloop-Gabriel-local\TEMPLATES_SUMMARY.md` | `//localhost` | `ref_generique` | 283 |
| `agent-multiloop-Gabriel-local\test-integration.sh` | `Connect` | `shell_appel` | 151 |
| `agent-multiloop-Gabriel-local\test-integration.sh` | `See` | `shell_appel` | 152 |
| `agent-multiloop-Gabriel-local\tests\test_banque_qr_sentinelle.py` | `espace_philippot.thy` | `chemin_litteral` | 195 |
| `agent-multiloop-Gabriel-local\tests\test_banque_qr_sentinelle.py` | `mecanique_discret.thy` | `chemin_litteral` | 196 |
| `agent-multiloop-Gabriel-local\tests\test_banque_qr_sentinelle.py` | `postulat_carre.thy` | `chemin_litteral` | 197 |
| `agent-multiloop-Gabriel-local\tests\test_cartouche_uniforme_ascii.py` | `/app/agent-multiloop-Gabriel-local` | `Path()` | 180 |
| `agent-multiloop-Gabriel-local\tests\test_ci_status.py` | `/nonexistent/tests/path` | `Path()` | 55 |
| `agent-multiloop-Gabriel-local\tests\test_ci_status.py` | `test_dummy.py` | `chemin_litteral` | 37 |
| `agent-multiloop-Gabriel-local\tests\test_cognitive.py` | `stats.json` | `chemin_litteral` | 149 |
| `agent-multiloop-Gabriel-local\tests\test_cognitive.py` | `s.json` | `chemin_litteral` | 194 |
| `agent-multiloop-Gabriel-local\tests\test_debat_orchestrator.py` | `data/debats` | `Path()` | 342 |
| `agent-multiloop-Gabriel-local\tests\test_debug_toolkit.py` | `z3-solver devrait etre installe via requirements.txt` | `chemin_litteral` | 28 |
| `agent-multiloop-Gabriel-local\tests\test_env_config.py` | `/app/agent-multiloop-Gabriel-local` | `Path()` | 25 |
| `agent-multiloop-Gabriel-local\tests\test_env_config.py` | `/home/agent/app` | `Path()` | 26 |
| `agent-multiloop-Gabriel-local\tests\test_filesystem_access.py` | `test.md` | `chemin_litteral` | 30 |
| `agent-multiloop-Gabriel-local\tests\test_filesystem_access.py` | `n_existe_pas.txt` | `chemin_litteral` | 49 |
| `agent-multiloop-Gabriel-local\tests\test_filesystem_access.py` | `C:\\sub\\test.md` | `chemin_litteral` | 70 |
| `agent-multiloop-Gabriel-local\tests\test_filesystem_access.py` | `programme.py` | `chemin_litteral` | 93 |
| `agent-multiloop-Gabriel-local\tests\test_filesystem_access.py` | `enorme.md` | `chemin_litteral` | 101 |
| `agent-multiloop-Gabriel-local\tests\test_filesystem_access.py` | `grand.txt` | `chemin_litteral` | 112 |
| `agent-multiloop-Gabriel-local\tests\test_filesystem_access.py` | `a.txt` | `chemin_litteral` | 125 |
| `agent-multiloop-Gabriel-local\tests\test_filesystem_access.py` | `fichier.txt` | `chemin_litteral` | 138 |
| `agent-multiloop-Gabriel-local\tests\test_filesystem_access.py` | `a.md` | `chemin_litteral` | 210 |
| `agent-multiloop-Gabriel-local\tests\test_filesystem_access.py` | `t.py` | `chemin_litteral` | 218 |
| `agent-multiloop-Gabriel-local\tests\test_forbidden_vocab_centralized.py` | `src/multiloop/critic.py` | `chemin_litteral` | 133 |
| `agent-multiloop-Gabriel-local\tests\test_forbidden_vocab_centralized.py` | `src/multiloop/coherence_detector.py` | `chemin_litteral` | 143 |
| `agent-multiloop-Gabriel-local\tests\test_forbidden_vocab_centralized.py` | `src/core/spectral_core.py` | `chemin_litteral` | 153 |
| `agent-multiloop-Gabriel-local\tests\test_forbidden_vocab_centralized.py` | `src/adapters/corpus/certainty_kernel.py` | `chemin_litteral` | 173 |
| `agent-multiloop-Gabriel-local\tests\test_forbidden_vocab_centralized.py` | `src/multiloop/slow_motion_debugger.py` | `chemin_litteral` | 190 |
| `agent-multiloop-Gabriel-local\tests\test_forbidden_vocab_centralized.py` | `src/spectral/spectral_knowledge.py` | `chemin_litteral` | 208 |
| `agent-multiloop-Gabriel-local\tests\test_image_command_windows_routing.py` | `/home/agent/app/data/theorie-savard/assets/images/figure.png` | `Path()` | 197 |
| `agent-multiloop-Gabriel-local\tests\test_image_command_windows_routing.py` | `/tmp/figure.png` | `chemin_litteral` | 147 |
| `agent-multiloop-Gabriel-local\tests\test_image_command_windows_routing.py` | `fichier.txt` | `chemin_litteral` | 185 |
| `agent-multiloop-Gabriel-local\tests\test_image_command_windows_routing.py` | `c:/dossier/fichier.txt` | `chemin_litteral` | 190 |
| `agent-multiloop-Gabriel-local\tests\test_keybindings.py` | `/tmp/test_gabriel_history_xyz` | `chemin_litteral` | 55 |
| `agent-multiloop-Gabriel-local\tests\test_keybindings.py` | `/tmp/different_path_ignored` | `chemin_litteral` | 58 |
| `agent-multiloop-Gabriel-local\tests\test_paths_resolution_container_fix.py` | `/app/agent-multiloop-Gabriel-local/CONFIG_ENV_GUIDE.md` | `Path()` | 13 |
| `agent-multiloop-Gabriel-local\tests\test_paths_resolution_container_fix.py` | `/home/agent/app/theories` | `chemin_litteral` | 135 |
| `agent-multiloop-Gabriel-local\tests\test_paths_resolution_container_fix.py` | `/home/agent/app/theories pour la coherence des tests.` | `chemin_litteral` | 137 |
| `agent-multiloop-Gabriel-local\tests\test_paths_resolution_container_fix.py` | `/home/agent/app/scripts` | `chemin_litteral` | 149 |
| `agent-multiloop-Gabriel-local\tests\test_paths_resolution_container_fix.py` | `/home/agent/app/memory` | `chemin_litteral` | 156 |
| `agent-multiloop-Gabriel-local\tests\test_pre_reasoner_v334.py` | `/rapide résume la section XIII` | `chemin_litteral` | 227 |
| `agent-multiloop-Gabriel-local\tests\test_pre_reasoner_v334.py` | `/standard calcule RsP(5,7)` | `chemin_litteral` | 232 |
| `agent-multiloop-Gabriel-local\tests\test_pre_reasoner_v334.py` | `/approfondi symétrique 3x3` | `chemin_litteral` | 237 |
| `agent-multiloop-Gabriel-local\tests\test_pre_reasoner_v334.py` | `/complet zeta et Riemann` | `chemin_litteral` | 242 |
| `agent-multiloop-Gabriel-local\tests\test_pre_reasoner_v334.py` | `/rapide` | `chemin_litteral` | 252 |
| `agent-multiloop-Gabriel-local\tests\test_section_XI_XII_integration.py` | `/theories` | `Path()` | 34 |
| `agent-multiloop-Gabriel-local\tests\test_section_XI_XII_integration.py` | `/home/agent/app/theories` | `Path()` | 35 |
| `agent-multiloop-Gabriel-local\tests\test_section_XI_XII_integration.py` | `/app/agent-multiloop-Gabriel-local/theories` | `Path()` | 36 |
| `agent-multiloop-Gabriel-local\tests\test_section_XI_XII_integration.py` | `/home/agent/app/scripts/isabelle_static_check.py` | `Path()` | 198 |
| `agent-multiloop-Gabriel-local\tests\test_section_XI_XII_integration.py` | `/app/agent-multiloop-Gabriel-local/scripts/isabelle_static_check.py` | `Path()` | 199 |
| `agent-multiloop-Gabriel-local\tests\test_slow_motion_debugger.py` | `/theories` | `Path()` | 36 |
| `agent-multiloop-Gabriel-local\tests\test_slow_motion_debugger.py` | `/home/agent/app/theories` | `Path()` | 37 |
| `agent-multiloop-Gabriel-local\tests\test_slow_motion_debugger.py` | `/app/agent-multiloop-Gabriel-local/theories` | `Path()` | 38 |
| `agent-multiloop-Gabriel-local\tests\test_ui_pro_banner_and_memoire.py` | `emergent.sh` | `chemin_litteral` | 30 |
| `agent-multiloop-Gabriel-local\tests\test_validation16_savard_and_build_workflow.py` | `./theories` | `chemin_litteral` | 34 |
| `agent-multiloop-Gabriel-local\tests\test_validation16_savard_and_build_workflow.py` | `La definition Savard `{name}` doit exister dans methode_spectral.thy` | `chemin_litteral` | 72 |
| `agent-multiloop-Gabriel-local\tests\test_validation16_savard_and_build_workflow.py` | `Le lemme/theoreme `{name}` doit exister dans methode_spectral.thy` | `chemin_litteral` | 114 |
| `agent-multiloop-Gabriel-local\tests\test_validation16_savard_and_build_workflow.py` | `Tactique Lean 4 interdite `{forbidden}` detectee dans .thy` | `chemin_litteral` | 185 |
| `agent-multiloop-Gabriel-local\tests\test_validation16_savard_and_build_workflow.py` | `elan-init.sh` | `chemin_litteral` | 246 |
| `agent-multiloop-Gabriel-local\tests\test_validation16_savard_and_build_workflow.py` | `sha256sum theories/methode_spectral.thy` | `chemin_litteral` | 249 |
| `agent-multiloop-Gabriel-local\tests\test_validation16_savard_and_build_workflow.py` | `theories/methode_spectral.thy` | `chemin_litteral` | 256 |
| `agent-multiloop-Gabriel-local\tests\test_validation16_savard_and_build_workflow.py` | `SHA256SUMS.txt` | `chemin_litteral` | 261 |
| `agent-multiloop-Gabriel-local\tests\test_verify_thy_structure.py` | `test.thy` | `chemin_litteral` | 35 |
| `agent-multiloop-Gabriel-local\tests\test_workflow_2025_2_contract.py` | `/home/agent/app/.github/workflows/build.yml` | `Path()` | 6 |
| `agent-multiloop-Gabriel-local\tests\test_workflow_2025_2_contract.py` | `/tmp/isabelle/Isabelle2025-2/bin` | `chemin_litteral` | 20 |
| `agent-multiloop-Gabriel-local\tests\test_workflow_2025_2_contract.py` | `/tmp/isabelle/Isabelle2025-2/bin/isabelle version` | `chemin_litteral` | 21 |
| `agent-multiloop-Gabriel-local\tests\test_workflow_2025_2_contract.py` | `subject-path: agent-multiloop-Gabriel-local/theories/methode_spectral.thy` | `chemin_litteral` | 41 |
| `agent-multiloop-Gabriel-local\tests\test_workflow_isabelle_syntax.py` | `/app` | `Path()` | 19 |
| `agent-multiloop-Gabriel-local\tests\test_workflow_isabelle_syntax.py` | `*.yml` | `chemin_litteral` | 35 |
| `agent-multiloop-Gabriel-local\tests\test_workflow_isabelle_syntax.py` | `isabelle\s+process\s+-T\s+\S+\.thy` | `chemin_litteral` | 49 |
| `agent-multiloop-Gabriel-local\tests\test_workflow_isabelle_syntax.py` | `src/hol/methode_spectral.thy` | `chemin_litteral` | 113 |
| `agent-multiloop-Gabriel-local\tests\test_workflow_isabelle_syntax.py` | `theories/methode_spectral.thy` | `chemin_litteral` | 212 |
| `agent-multiloop-Gabriel-local\theories\geometrie_spectre_premier.thy` | `Complex_Main` | `thy_import` | 1 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_02.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_03.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_04.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_05.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_06.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_07.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_08.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_09.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_10.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_100.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_11.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_12.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_13.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_14.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_15.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_16.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_17.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_18.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_19.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_20.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_21.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_22.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_23.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_24.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_25.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_26.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_27.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_28.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_29.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_30.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_31.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_32.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_33.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_34.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_35.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_36.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_37.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_38.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_39.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_40.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_41.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_42.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_43.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_44.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_45.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_46.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_47.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_48.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_49.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_50.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_51.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_52.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_53.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_54.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_55.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_56.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_57.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_58.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_59.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_60.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_61.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_62.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_63.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_64.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_65.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_66.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_67.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_68.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_69.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_70.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_71.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_72.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_73.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_74.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_75.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_76.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_77.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_78.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_79.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_80.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_81.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_82.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_83.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_84.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_85.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_86.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_87.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_88.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_89.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_90.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_91.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_92.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_93.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_94.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_95.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_96.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_97.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_98.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_99.thy` | `Main` | `thy_import` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\scripts\script_savard_01.sh` | `A` | `shell_appel` | 4 |
| `agent-multiloop-Gabriel-local\theories\projects\scripts\script_savard_02.sh` | `A` | `shell_appel` | 4 |
| `agent-multiloop-Gabriel-local\theories\projects\scripts\script_savard_03.sh` | `A` | `shell_appel` | 4 |
| `agent-multiloop-Gabriel-local\theories\projects\scripts\script_savard_04.sh` | `A` | `shell_appel` | 4 |
| `agent-multiloop-Gabriel-local\theories\projects\scripts\script_savard_05.sh` | `A` | `shell_appel` | 4 |
| `agent-multiloop-Gabriel-local\theories\projects\scripts\script_savard_06.sh` | `A` | `shell_appel` | 4 |
| `agent-multiloop-Gabriel-local\theories\projects\scripts\script_savard_07.sh` | `A` | `shell_appel` | 4 |
| `agent-multiloop-Gabriel-local\theories\projects\scripts\script_savard_08.sh` | `A` | `shell_appel` | 4 |
| `agent-multiloop-Gabriel-local\theories\projects\scripts\script_savard_09.sh` | `A` | `shell_appel` | 4 |
| `agent-multiloop-Gabriel-local\theories\projects\scripts\script_savard_10.sh` | `A` | `shell_appel` | 4 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_01.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_01.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_01.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_01.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_01.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_02.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_02.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_02.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_02.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_02.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_03.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_03.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_03.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_03.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_03.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_04.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_04.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_04.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_04.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_04.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_05.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_05.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_05.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_05.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_05.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_06.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_06.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_06.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_06.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_06.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_07.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_07.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_07.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_07.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_07.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_08.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_08.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_08.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_08.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_08.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_09.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_09.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_09.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_09.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_09.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_10.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_10.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_10.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_10.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_10.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_100.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_100.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_100.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_100.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_100.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_11.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_11.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_11.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_11.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_11.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_12.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_12.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_12.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_12.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_12.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_13.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_13.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_13.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_13.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_13.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_14.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_14.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_14.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_14.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_14.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_15.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_15.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_15.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_15.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_15.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_16.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_16.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_16.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_16.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_16.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_17.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_17.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_17.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_17.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_17.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_18.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_18.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_18.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_18.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_18.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_19.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_19.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_19.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_19.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_19.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_20.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_20.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_20.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_20.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_20.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_21.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_21.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_21.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_21.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_21.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_22.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_22.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_22.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_22.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_22.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_23.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_23.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_23.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_23.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_23.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_24.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_24.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_24.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_24.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_24.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_25.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_25.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_25.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_25.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_25.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_26.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_26.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_26.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_26.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_26.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_27.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_27.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_27.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_27.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_27.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_28.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_28.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_28.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_28.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_28.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_29.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_29.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_29.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_29.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_29.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_30.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_30.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_30.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_30.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_30.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_31.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_31.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_31.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_31.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_31.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_32.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_32.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_32.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_32.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_32.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_33.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_33.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_33.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_33.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_33.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_34.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_34.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_34.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_34.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_34.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_35.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_35.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_35.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_35.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_35.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_36.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_36.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_36.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_36.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_36.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_37.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_37.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_37.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_37.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_37.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_38.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_38.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_38.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_38.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_38.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_39.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_39.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_39.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_39.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_39.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_40.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_40.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_40.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_40.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_40.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_41.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_41.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_41.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_41.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_41.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_42.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_42.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_42.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_42.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_42.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_43.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_43.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_43.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_43.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_43.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_44.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_44.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_44.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_44.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_44.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_45.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_45.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_45.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_45.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_45.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_46.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_46.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_46.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_46.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_46.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_47.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_47.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_47.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_47.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_47.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_48.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_48.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_48.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_48.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_48.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_49.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_49.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_49.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_49.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_49.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_50.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_50.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_50.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_50.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_50.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_51.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_51.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_51.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_51.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_51.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_52.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_52.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_52.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_52.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_52.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_53.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_53.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_53.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_53.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_53.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_54.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_54.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_54.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_54.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_54.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_55.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_55.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_55.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_55.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_55.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_56.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_56.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_56.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_56.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_56.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_57.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_57.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_57.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_57.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_57.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_58.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_58.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_58.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_58.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_58.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_59.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_59.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_59.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_59.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_59.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_60.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_60.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_60.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_60.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_60.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_61.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_61.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_61.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_61.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_61.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_62.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_62.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_62.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_62.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_62.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_63.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_63.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_63.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_63.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_63.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_64.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_64.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_64.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_64.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_64.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_65.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_65.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_65.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_65.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_65.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_66.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_66.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_66.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_66.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_66.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_67.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_67.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_67.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_67.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_67.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_68.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_68.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_68.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_68.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_68.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_69.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_69.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_69.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_69.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_69.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_70.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_70.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_70.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_70.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_70.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_71.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_71.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_71.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_71.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_71.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_72.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_72.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_72.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_72.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_72.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_73.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_73.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_73.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_73.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_73.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_74.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_74.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_74.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_74.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_74.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_75.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_75.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_75.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_75.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_75.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_76.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_76.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_76.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_76.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_76.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_77.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_77.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_77.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_77.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_77.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_78.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_78.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_78.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_78.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_78.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_79.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_79.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_79.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_79.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_79.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_80.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_80.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_80.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_80.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_80.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_81.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_81.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_81.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_81.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_81.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_82.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_82.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_82.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_82.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_82.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_83.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_83.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_83.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_83.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_83.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_84.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_84.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_84.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_84.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_84.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_85.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_85.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_85.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_85.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_85.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_86.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_86.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_86.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_86.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_86.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_87.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_87.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_87.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_87.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_87.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_88.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_88.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_88.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_88.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_88.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_89.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_89.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_89.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_89.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_89.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_90.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_90.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_90.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_90.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_90.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_91.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_91.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_91.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_91.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_91.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_92.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_92.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_92.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_92.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_92.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_93.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_93.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_93.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_93.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_93.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_94.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_94.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_94.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_94.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_94.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_95.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_95.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_95.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_95.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_95.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_96.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_96.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_96.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_96.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_96.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_97.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_97.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_97.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_97.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_97.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_98.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_98.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_98.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_98.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_98.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_99.tex` | `inputenc` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_99.tex` | `babel` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_99.tex` | `amsmath` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_99.tex` | `amssymb` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_99.tex` | `geometry` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\README_LEAN.md` | `//raw.githubusercontent.com/leanprover/elan/master/elan-init.sh` | `ref_generique` | 20 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `inputenc` | `latex_inclusion` | 2 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `fontenc` | `latex_inclusion` | 3 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `babel` | `latex_inclusion` | 4 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `lmodern` | `latex_inclusion` | 5 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `amsmath` | `latex_inclusion` | 6 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `amssymb` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `xcolor` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `geometry` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `hyperref` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `longtable` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `array` | `latex_inclusion` | 12 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `booktabs` | `latex_inclusion` | 13 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `enumitem` | `latex_inclusion` | 14 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `titlesec` | `latex_inclusion` | 15 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `tocloft` | `latex_inclusion` | 16 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `setspace` | `latex_inclusion` | 17 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `microtype` | `latex_inclusion` | 18 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `etoolbox` | `latex_inclusion` | 19 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `fancyhdr` | `latex_inclusion` | 20 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `xurl` | `latex_inclusion` | 21 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `underscore` | `latex_inclusion` | 22 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `listings` | `latex_inclusion` | 23 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `tcolorbox` | `latex_inclusion` | 24 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex` | `newunicodechar` | `latex_inclusion` | 25 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | ` Copilot — Microsoft E1 — emergent.sh Gordon — Docker Desktop Claude API — Anthropic Gemini — Google Ces co-auteurs ont contribué à la formalisation Isabelle/HOL, à la rédaction assistée, à la vérification des preuves , chacun à part égale avec l'auteur principal.` | `json_chemin` | 17 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | ` Copilot — Microsoft E1 — émergent.sh Gordon — Docker Desktop Claude API — Anthropic Gemini — Google Ces co-auteurs ont contribué à la formalisation Isabelle/HOL, à la rédaction assistée, à la vérification des preuves , chacun à part égale avec l'auteur principal.` | `json_chemin` | 18 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `Note liminaire \\\\ Ce document contient des formules, des preuves formelles validées par Isabelle/HOL, et la voix de l'auteur, qui cherche à faire toucher au lecteur ce que la géométrie des nombres premiers lui a fait ressentir. Cette géométrie est la chair qui le touche et qu'il touche en retour. Toute est tiré des documents sources et du fichier methode spectrale. Vous êtes invités a consulter les fichiers Readme des dépôts publics mise en place et à la dispositon des contributeur via PR, de partager, consulter, cloner, selon les permissions de la LICENSE Apach 2.0 Bienvenu a tous.\\_spectral.thy validé par l'assistant de preuve. Méthode Spectrale de Philippe Thomas Savard.` | `json_chemin` | 57 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `Note liminaire \\\\ Ce document contient des formules, des preuves formelles validées par Isabelle/HOL, et la voix de l'auteur, qui cherche à faire toucher au lecteur ce que la géométrie des nombres premiers lui a fait ressentir. Cette géométrie est la chair qui le touche et qu'il touche en retour. Tout est tiré des documents sources et du fichier méthode spectrale. Vous êtes invités à consulter les fichiers README des dépôts publics mise à disposition des contributeurs via PR, de partager, consulter, cloner, selon les permissions de la LICENSE Apache 2.0 Bienvenue à tous.\\_spectral.thy validé par l'assistant de preuve. Méthode Spectrale de Philippe Thomas Savard.` | `json_chemin` | 58 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `Le code Isabelle/HOL correspondant, tiré du fichier methode\\_spectral.thy (Section XII, lignes 365–382), est le suivant :` | `json_chemin` | 287 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `Le code Isabelle/HOL correspondant, tiré du fichier méthode\\_spectral.thy (Section XII, lignes 365–382), est le suivant :` | `json_chemin` | 288 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `Valeurs de référence \\\\ Pour n = 10 : SA(10) = 1 662 et SB(10) = 3 262. Pour n = 11 : SA(11) = 3 326 et SB(11) = 6 590. Ces valeurs sont prouvées formellement par les lemmes SA\\_10, SA\\_11, SB\\_10, SB\\_11 dans le fichier methode\\_spectral.thy.` | `json_chemin` | 377 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `Valeurs de référence \\\\ Pour n = 10 : SA(10) = 1 662 et SB(10) = 3 262. Pour n = 11 : SA(11) = 3 326 et SB(11) = 6 590. Ces valeurs sont prouvées formellement par les femmes SA\\_10, SA\\_11, SB\\_10, SB\\_11 dans le fichier méthode\\_spectral.thy.` | `json_chemin` | 378 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `Ces cinq résultats sont prouvés formellement par les lemmes SA\\_9 à SA\\_13, SB\\_9 à SB\\_13, et digamma\\_calc\\_23 à digamma\\_calc\\_41 dans le fichier methode\\_spectral.thy. Chaque preuve HOL constitue une certification machinique de l'exactitude du calcul.` | `json_chemin` | 627 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `Ces cinq résultats sont prouvés formellement par les femmes SA\\_9 à SA\\_13, SB\\_9 à SB\\_13, et digamma\\_calc\\_23 à digamma\\_calc\\_41 dans le fichier méthode\\_spectral.thy. Chaque preuve HOL constitue une certification machiniste de l'exactitude du calcul.` | `json_chemin` | 628 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `(* Extraits de methode_spectral.thy, section I.5 *)` | `json_chemin` | 637 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `(* Extraits de méthode_spectral.thy, section I.5 *)` | `json_chemin` | 638 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `(* Schema de preuve utilise dans methode_spectral.thy *)` | `json_chemin` | 727 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `(* Schema de preuve utilise dans méthode_spectral.thy *)` | `json_chemin` | 728 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `« La Méthode Spectrale caractérise EXACTEMENT l'ensemble ℙ des nombres premiers — ni plus, ni moins — dans ses trois domaines d'application. » \\\\ — Synthèse formelle, fichier methode\\_spectral.thy, juillet 2026` | `json_chemin` | 787 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `« La Méthode Spectrale caractérise EXACTEMENT l'ensemble ℙ des nombres premiers — ni plus, ni moins — dans ses trois domaines d'application. » \\\\ — Synthèse formelle, fichier méthode\\_spectral.thy, juillet 2026` | `json_chemin` | 788 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `Le théorème de synthèse est le point culminant du fichier methode\\_spectral.thy (version 3.42). Il constitue un ensemble à lui seul : il agrège les cinq faits indépendamment démontrés dans ce fichier en un seul énoncé unifié.` | `json_chemin` | 847 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `Le théorème de synthèse est le point culminant du fichier méthode\\_spectral.thy (version 3.42). Il constitue un ensemble à lui seul : il agrège les cinq faits indépendamment démontrés dans ce fichier en un seul énoncé unifié.` | `json_chemin` | 848 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `Chacun de ces faits est déjà un théorème ou un lemme HOL prouvé dans les sections précédentes du fichier methode\\_spectral.thy. Le théorème de synthèse se contente de les assembler — il n'introduit aucun axiome nouveau.` | `json_chemin` | 857 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `Chacun de ces faits est déjà un théorème ou un femme HOL prouvé dans les sections précédentes du fichier méthode\\_spectral.thy. Le théorème de synthèse se contente de les assembler — il n'introduit aucun axiome nouveau.` | `json_chemin` | 858 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `(* Pour F1 et F3 : voir les lemmes du Pont Savard (Section XIII) dans methode_spectral.thy *)` | `json_chemin` | 877 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `(* Pour F1 et F3 : voir les femmes du Pont Savard (Section XIII) dans méthode_spectral.thy *)` | `json_chemin` | 878 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `Fait & Énoncé & Source dans methode\\_spectral.thy` | `json_chemin` | 887 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `Fait & Énoncé & Source dans méthode\\_spectral.thy` | `json_chemin` | 888 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `Le tableau suivant constitue un index de navigation vers les six postulats fondamentaux et leurs réalisations formelles dans methode\\_spectral.thy :` | `json_chemin` | 1127 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `Le tableau suivant constitue un index de navigation vers les six postulats fondamentaux et leurs réalisations formelles dans méthode\\_spectral.thy :` | `json_chemin` | 1128 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `Copyright 2026 Philippe Thomas Savard \\\\ Le fichier methode\\_spectral.thy et le présent document sont distribués sous les termes de la Licence Apache, Version 2.0 (la « Licence »). Vous ne pouvez utiliser ce fichier qu'en conformité avec la Licence. \\\\ Vous pouvez obtenir une copie de la Licence à l'adresse : \\\\ http://www.apache.org/licenses/LICENSE-2.0 \\\\ Sauf si requis par la loi applicable ou convenu par écrit, le logiciel distribué sous la Licence est distribué « EN L'ÉTAT », SANS GARANTIES NI CONDITIONS D'AUCUNE SORTE, expresses ou implicites. Voir la Licence pour les dispositions spécifiques régissant les autorisations et limitations en vertu de la Licence. \\\\ Dépôt public : https://github.com/PhilippeThomasSavard/Agent-multiloop-Gabriel` | `json_chemin` | 1197 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json` | `Copyright 2026 Philippe Thomas Savard \\\\ Le fichier méthode\\_spectral.thy et le présent document sont distribués sous les termes de la Licence Apache, Version 2.0 (la « Licence »). Vous ne pouvez utiliser ce fichier qu'en conformité avec la Licence. \\\\ Vous pouvez obtenir une copie de la Licence à l'adresse : \\\\ hâte://www.apache.org/licences/LICENSE-2.0 \\\\ Sauf si requis par la loi applicable ou convenu par écrit, le logiciel distribué sous la Licence est distribué « EN L'ÉTAT », SANS GARANTIES NI CONDITIONS D'AUCUNE SORTE, expresses ou implicites. Voir la Licence pour les dispositions spécifiques régissant les autorisations et limitations en vertu de la Licence. \\\\ Dépôt public : hôtes://github.com/PhilippeThomasSavard/Agent-multiloop-Gabriel` | `json_chemin` | 1198 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | ` Copilot — Microsoft E1 — emergent.sh Gordon — Docker Desktop Claude API — Anthropic Gemini — Google Ces co-auteurs ont contribué à la formalisation Isabelle/HOL, à la rédaction assistée, à la vérification des preuves , chacun à part égale avec l'auteur principal.` | `json_chemin` | 57 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | ` Copilote — Microsoft E1 — émergent.sh Cordon — Docker Desktop Claude API — Anthropic Gamin — Gorge Ces co-auteurs ont contribué à la formalisation Isabelle/HOL, à la rédaction assistée, à la vérification des preuves , chacun à part égale avec l'auteur principal.` | `json_chemin` | 58 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `Note liminaire \\\\ Ce document contient des formules, des preuves formelles validées par Isabelle/HOL, et la voix de l'auteur, qui cherche à faire toucher au lecteur ce que la géométrie des nombres premiers lui a fait ressentir. Cette géométrie est la chair qui le touche et qu'il touche en retour. Toute est tiré des documents sources et du fichier methode. Vous êtes invités a consulter les fichiers Readme des dépôts publics mise en place et à la dispositon des contributeur via PR, de partager, consulter, cloner, selon les permissions de la LICENSE Apach 2.0 Bienvenu a tous.\\_spectral.thy validé par l'assistant de preuve. Méthode Spectrale de Philippe Thomas Savard.` | `json_chemin` | 107 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `Note liminaire \\\\ Ce document contient des formules, des preuves formelles validées par Isabelle/HOL, et la voix de l'auteur, qui cherche à faire toucher au lecteur ce que la géométrie des nombres premiers lui a fait ressentir. Cette géométrie est la chair qui le touche et qu'il touche en retour. Tout est tiré des documents sources et du fichier méthode. Vous êtes invités à consulter les fichiers README des dépôts publics mise à disposition des contributeurs via PR, de partager, consulter, cloner, selon les permissions de la LICENSE Apache 2.0 Bienvenue à tous.\\_spectral.thy validé par l'assistant de preuve. Méthode Spectrale de Philippe Thorax Bavard.` | `json_chemin` | 108 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `Le code Isabelle/HOL correspondant, tiré du fichier methode\\_spectral.thy (Section XII, lignes 365–382), est le suivant :` | `json_chemin` | 377 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `Le code Isabelle/HOL correspondant, tiré du fichier méthode\\_spectral.thy (Section XII, lignes 365–382), est le suivant :` | `json_chemin` | 378 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `Valeurs de référence \\\\ Pour n = 10 : SA(10) = 1 662 et SB(10) = 3 262. Pour n = 11 : SA(11) = 3 326 et SB(11) = 6 590. Ces valeurs sont prouvées formellement par les lemmes SA\\_10, SA\\_11, SB\\_10, SB\\_11 dans le fichier methode\\_spectral.thy.` | `json_chemin` | 467 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `Valeurs de référence \\\\ Pour n = 10 : SA(10) = 1 662 et SB(10) = 3 262. Pour n = 11 : SA(11) = 3 326 et SB(11) = 6 590. Ces valeurs sont prouvées formellement par les femmes SA\\_10, SA\\_11, SB\\_10, SB\\_11 dans le fichier méthode\\_spectral.thy.` | `json_chemin` | 468 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `Ces cinq résultats sont prouvés formellement par les lemmes SA\\_9 à SA\\_13, SB\\_9 à SB\\_13, et digamma\\_calc\\_23 à digamma\\_calc\\_41 dans le fichier methode\\_spectral.thy. Chaque preuve HOL constitue une certification machinique de l'exactitude du calcul.` | `json_chemin` | 727 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `Ces cinq résultats sont prouvés formellement par les femmes SA\\_9 à SA\\_13, SB\\_9 à SB\\_13, et digamma\\_calc\\_23 à digamma\\_calc\\_41 dans le fichier méthode\\_spectral.thy. Chaque preuve HOL constitue une certification machiniste de l'exactitude du calcul.` | `json_chemin` | 728 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `(* Extraits de methode_spectral.thy, section I.5 *)` | `json_chemin` | 737 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `(* Extraits de méthode_spectral.thy, section I.5 *)` | `json_chemin` | 738 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `(* Schema de preuve utilise dans methode_spectral.thy *)` | `json_chemin` | 827 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `(* Schéma de preuve utilise dans méthode_spectral.thy *)` | `json_chemin` | 828 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `« La Méthode Spectrale caractérise EXACTEMENT l'ensemble ℙ des nombres premiers — ni plus, ni moins — dans ses trois domaines d'application. » \\\\ — Synthèse formelle, fichier methode\\_spectral.thy, juillet 2026` | `json_chemin` | 897 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `« La Méthode Spectrale caractérise EXACTEMENT l'ensemble ℙ des nombres premiers — ni plus, ni moins — dans ses trois domaines d'application. » \\\\ — Synthèse formelle, fichier méthode\\_spectral.thy, juillet 2026` | `json_chemin` | 898 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `Le théorème de synthèse est le point culminant du fichier methode\\_spectral.thy (version 3.42). Il constitue un ensemble à lui seul : il agrège les cinq faits indépendamment démontrés dans ce fichier en un seul énoncé unifié.` | `json_chemin` | 1017 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `Le théorème de synthèse est le point culminant du fichier méthode\\_spectral.thy (version 3.42). Il constitue un ensemble à lui seul : il agrège les cinq faits indépendamment démontrés dans ce fichier en un seul énoncé unifié.` | `json_chemin` | 1018 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `Chacun de ces faits est déjà un théorème ou un lemme HOL prouvé dans les sections précédentes du fichier methode\\_spectral.thy. Le théorème de synthèse se contente de les assembler — il n'introduit aucun axiome nouveau.` | `json_chemin` | 1027 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `Chacun de ces faits est déjà un théorème ou un femme HOL prouvé dans les sections précédentes du fichier méthode\\_spectral.thy. Le théorème de synthèse se contente de les assembler — il n'introduit aucun axiome nouveau.` | `json_chemin` | 1028 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `(* Pour F1 et F3 : voir les lemmes du Pont Savard (Section XIII) dans methode_spectral.thy *)` | `json_chemin` | 1047 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `(* Pour F1 et F3 : voir les femmes du Pont Bavard (Section XIII) dans méthode_spectral.thy *)` | `json_chemin` | 1048 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `Fait & Énoncé & Source dans methode\\_spectral.thy` | `json_chemin` | 1057 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `Fait & Énoncé & Source dans méthode\\_spectral.thy` | `json_chemin` | 1058 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `Le tableau suivant constitue un index de navigation vers les six postulats fondamentaux et leurs réalisations formelles dans methode\\_spectral.thy :` | `json_chemin` | 1347 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `Le tableau suivant constitue un index de navigation vers les six postulats fondamentaux et leurs réalisations formelles dans méthode\\_spectral.thy :` | `json_chemin` | 1348 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `Copyright 2026 Philippe Thomas Savard \\\\ Le fichier methode\\_spectral.thy et le présent document sont distribués sous les termes de la Licence Apache, Version 2.0 (la « Licence »). Vous ne pouvez utiliser ce fichier qu'en conformité avec la Licence. \\\\ Vous pouvez obtenir une copie de la Licence à l'adresse : \\\\ http://www.apache.org/licenses/LICENSE-2.0 \\\\ Sauf si requis par la loi applicable ou convenu par écrit, le logiciel distribué sous la Licence est distribué « EN L'ÉTAT », SANS GARANTIES NI CONDITIONS D'AUCUNE SORTE, expresses ou implicites. Voir la Licence pour les dispositions spécifiques régissant les autorisations et limitations en vertu de la Licence. \\\\ Dépôt public : https://github.com/PhilippeThomasSavard/Agent-multiloop-Gabriel` | `json_chemin` | 1427 |
| `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json` | `Copyright 2026 Philippe Thorax Bavard \\\\ Le fichier méthode\\_spectral.thy et le présent document sont distribués sous les termes de la Licence Apache, Version 2.0 (la « Licence »). Vous ne pouvez utiliser ce fichier qu'en conformité avec la Licence. \\\\ Vous pouvez obtenir une copie de la Licence à l'adresse : \\\\ hâte://www.apache.org/licences/LICENSE-2.0 \\\\ Sauf si requis par la loi applicable ou convenu par écrit, le logiciel distribué sous la Licence est distribué « EN L'ÉTAT », SANS GARANTIES NI CONDITIONS D'AUCUNE SORTE, expresses ou implicites. Voir la Licence pour les dispositions spécifiques régissant les autorisations et limitations en vertu de la Licence. \\\\ Dépôt public : hôtes://github.com/PhilippeThomasSavard/Agent-multiloop-Gariez` | `json_chemin` | 1428 |
| `agent-multiloop-Gabriel-local\theories\tex\convert_docx_to_latex.py` | `.//w:t` | `chemin_litteral` | 150 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `inputenc` | `latex_inclusion` | 2 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `fontenc` | `latex_inclusion` | 3 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `babel` | `latex_inclusion` | 4 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `lmodern` | `latex_inclusion` | 5 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `amsmath` | `latex_inclusion` | 6 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `amssymb` | `latex_inclusion` | 7 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `xcolor` | `latex_inclusion` | 8 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `geometry` | `latex_inclusion` | 9 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `hyperref` | `latex_inclusion` | 10 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `longtable` | `latex_inclusion` | 11 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `array` | `latex_inclusion` | 12 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `booktabs` | `latex_inclusion` | 13 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `enumitem` | `latex_inclusion` | 14 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `titlesec` | `latex_inclusion` | 15 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `tocloft` | `latex_inclusion` | 16 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `setspace` | `latex_inclusion` | 17 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `microtype` | `latex_inclusion` | 18 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `etoolbox` | `latex_inclusion` | 19 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `fancyhdr` | `latex_inclusion` | 20 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `xurl` | `latex_inclusion` | 21 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `underscore` | `latex_inclusion` | 22 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `listings` | `latex_inclusion` | 23 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `tcolorbox` | `latex_inclusion` | 24 |
| `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex` | `newunicodechar` | `latex_inclusion` | 25 |
| `agent-multiloop-Gabriel-local\theories\tex\PDF\README_pdf.txt` | `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local.git` | `ref_generique` | 149 |
| `agent-multiloop-Gabriel-local\theories\tex\PDF\README_pdf.txt` | `//github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026.git` | `ref_generique` | 150 |
| `agent-multiloop-Gabriel-local\theories\tex\PDF\README_pdf.txt` | `//github.com/2racinede4carreunivers-dev/Ia_geo_spec_prem_app_deplo.git` | `ref_generique` | 151 |
| `agent-multiloop-Gabriel-local\theories\tex\PDF\README_pdf.txt` | `//www.universestaucarre.com` | `ref_generique` | 152 |
| `agent-multiloop-Gabriel-local\theories\tex\tex_quality\quality_pipeline.py` | `r` | `open_fichier` | 109 |
| `agent-multiloop-Gabriel-local\theories\validation_hol_unifiee.thy` | `Complex_Main` | `thy_import` | 16 |
| `agent-multiloop-Gabriel-local\theories\validation_hol_unifiee.thy` | `Real` | `thy_import` | 16 |
| `agent-multiloop-Gabriel-local\theories\verify_thy_structure.py` | `Un probleme detecte dans le fichier .thy` | `chemin_litteral` | 220 |
| `agent-multiloop-Gabriel-local\theories\verify_thy_structure.py` | `Rapport agrege pour un fichier .thy` | `chemin_litteral` | 232 |
| `agent-multiloop-Gabriel-local\theories\verify_thy_structure.py` | `*.thy` | `chemin_litteral` | 764 |
| `agent-multiloop-Gabriel-local\TODO_ANALYSE.md` | `gabriel_llm_integration.py` | `ref_generique` | 60 |
| `agent-multiloop-Gabriel-local\TODO_ANALYSE.md` | `hol_proof_generator.py` | `ref_generique` | 64 |
| `agent-multiloop-Gabriel-local\TODO_ANALYSE.md` | `multiloop_validation_engine.py` | `ref_generique` | 68 |
| `agent-multiloop-Gabriel-local\TODO_ANALYSE.md` | `spectral_ratio_analyzer.py` | `ref_generique` | 70 |
| `agent-multiloop-Gabriel-local\UTF8_ENCODING_FIX.md` | `hashlib.sh` | `ref_generique` | 89 |
| `agent-multiloop-Gabriel-local\VERIFICATION_COMPLETE_RESULTAT_FINAL.md` | `DEMARRAGE_RAPIDE.md` | `ref_generique` | 113 |
| `agent-multiloop-Gabriel-local\VERIFICATION_COMPLETE_RESULTAT_FINAL.md` | `README_GUIDES.md` | `ref_generique` | 114 |
| `agent-multiloop-Gabriel-local\VERIFICATION_FINALE_SYNTHESE.txt` | `README_FINAL.md` | `ref_generique` | 108 |
| `ANALYSE_GITHUB_SYNC_FEASIBILITY.md` | `chaos_harmonic_discrete.thy` | `ref_generique` | 34 |
| `ANALYSE_GITHUB_SYNC_FEASIBILITY.md` | `universes_carre.thy` | `ref_generique` | 35 |
| `ANALYSE_GITHUB_SYNC_FEASIBILITY.md` | `/data/theories` | `ref_generique` | 103 |
| `ANALYSE_GITHUB_SYNC_FEASIBILITY.md` | `github_client.py` | `ref_generique` | 151 |
| `ANALYSE_GITHUB_SYNC_FEASIBILITY.md` | `git_sync_service.py` | `ref_generique` | 152 |
| `ANALYSE_GITHUB_SYNC_FEASIBILITY.md` | `conflict_resolver.py` | `ref_generique` | 153 |
| `ANALYSE_GITHUB_SYNC_FEASIBILITY.md` | `token_manager.py` | `ref_generique` | 154 |
| `ANALYSE_GITHUB_SYNC_FEASIBILITY.md` | `file_contents.sh` | `ref_generique` | 271 |
| `ANALYSE_GITHUB_SYNC_FEASIBILITY.md` | `gabriel-deployment.yaml` | `ref_generique` | 301 |
| `ANALYSE_GITHUB_SYNC_FEASIBILITY.md` | `sync-configmap.yaml` | `ref_generique` | 302 |
| `ANALYSE_GITHUB_SYNC_FEASIBILITY.md` | `github-secret.yaml` | `ref_generique` | 303 |
| `ANALYSE_GITHUB_SYNC_FEASIBILITY.md` | `services.yaml` | `ref_generique` | 304 |
| `ANALYSE_GITHUB_SYNC_FEASIBILITY.md` | `/cache/hol` | `ref_generique` | 335 |
| `ANALYSE_GITHUB_SYNC_FEASIBILITY.md` | `//github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026.git` | `ref_generique` | 409 |
| `ANALYSE_GITHUB_SYNC_FEASIBILITY.md` | `fichier.thy` | `ref_generique` | 427 |
| `ANALYSE_GITHUB_SYNC_FEASIBILITY.md` | `Emergent.sh` | `ref_generique` | 431 |
| `ANALYSE_RAPPORT_SESSION_GABRIEL_DISCRIMINATION.md` | `gabriel_multiloop.py` | `ref_generique` | 215 |
| `backend\server.py` | `/status` | `chemin_litteral` | 45 |
| `BADGE_SCIENTIFIQUE_IMPLEMENTATION.md` | `/app/logs/agent_cli.log` | `ref_generique` | 153 |
| `BILAN_COMPLET_SESSION.md` | `AUDIT_FICHIERS_ENV_COMPLET.md` | `ref_generique` | 94 |
| `BILAN_COMPLET_SESSION.md` | `RESOLUTION_ENV_ABSENT_AU_LANCEMENT.md` | `ref_generique` | 122 |
| `CHANGELOG.md` | `//keepachangelog.com/fr/1.1.0/` | `ref_generique` | 5 |
| `CHANGELOG.md` | `//semver.org/lang/fr/` | `ref_generique` | 6 |
| `CHANGELOG.md` | `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local` | `ref_generique` | 9 |
| `CONTRIBUTING.md` | `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local.git` | `ref_generique` | 74 |
| `CONTRIBUTING.md` | `//isabelle.in.tum.de/website-Isabelle2025-2/installation.html` | `ref_generique` | 86 |
| `CORRECTION_DEFINITIVE_LIGNE_2605.md` | `/cygdrive/c/agent-multiloop-Gabriel-local-final/agent-multiloop-Gabriel-local/theories` | `ref_generique` | 75 |
| `CORRECTIONS_APPLIQUEES_CONFIRMATION.md` | `/cygdrive/c/agent-multiloop-Gabriel-local-final/agent-multiloop-Gabriel-local/theories` | `ref_generique` | 93 |
| `declaration_securite.md` | `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local/issues/new` | `ref_generique` | 89 |
| `deploy_gabriel_v6.py` | `\n[STEP 1] Vérifier .env` | `chemin_litteral` | 21 |
| `DIAGNOSTIC_LLM_CONFLICT_OPENAI_ANTHROPIC.md` | `test_llm_routing.py` | `ref_generique` | 270 |
| `docs\index.html` | `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local` | `ref_generique` | 202 |
| `docs\index.html` | `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local/releases` | `ref_generique` | 203 |
| `docs\index.html` | `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local/blob/main/agent-multiloop-Gabriel-local/theories/methode_spectral.thy` | `ref_generique` | 204 |
| `docs\index.html` | `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local.git` | `ref_generique` | 280 |
| `docs\index.html` | `//www.apache.org/licenses/LICENSE-2.0` | `ref_generique` | 291 |
| `docs\index.html` | `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local/actions` | `ref_generique` | 329 |
| `docs\index.html` | `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local/blob/main/LICENSE` | `ref_generique` | 331 |
| `docs\README.md` | `//2racinede4carreunivers-dev.github.io/agent-multiloop-Gabriel-local/` | `ref_generique` | 14 |
| `frontend\components.json` | `https://ui.shadcn.com/schema.json` | `json_chemin` | 2 |
| `frontend\craco.config.js` | `process.env` | `ref_generique` | 7 |
| `frontend\craco.config.js` | `./plugins/health-check/webpack-health-plugin` | `ref_generique` | 20 |
| `frontend\craco.config.js` | `./plugins/health-check/health-endpoints` | `ref_generique` | 21 |
| `frontend\package.json` | `https://assets.emergent.sh/npm/emergentbase-visual-edits-1.0.8.tgz` | `json_chemin` | 83 |
| `frontend\plugins\health-check\health-endpoints.js` | `/health` | `ref_generique` | 27 |
| `frontend\plugins\health-check\health-endpoints.js` | `res.json` | `ref_generique` | 34 |
| `frontend\plugins\health-check\health-endpoints.js` | `process.env` | `ref_generique` | 78 |
| `frontend\plugins\health-check\health-endpoints.js` | `/health/simple` | `ref_generique` | 83 |
| `frontend\plugins\health-check\health-endpoints.js` | `/health/ready` | `ref_generique` | 100 |
| `frontend\plugins\health-check\health-endpoints.js` | `/health/live` | `ref_generique` | 122 |
| `frontend\plugins\health-check\health-endpoints.js` | `/health/errors` | `ref_generique` | 132 |
| `frontend\plugins\health-check\health-endpoints.js` | `/health/stats` | `ref_generique` | 147 |
| `frontend\public\index.html` | `emergent.sh` | `ref_generique` | 7 |
| `frontend\public\index.html` | `//fonts.googleapis.com` | `ref_generique` | 8 |
| `frontend\public\index.html` | `//fonts.gstatic.com` | `ref_generique` | 9 |
| `frontend\public\index.html` | `//fonts.googleapis.com/css2` | `ref_generique` | 10 |
| `frontend\public\index.html` | `manifest.json` | `ref_generique` | 12 |
| `frontend\public\index.html` | `//developers.google.com/web/fundamentals/web-app-manifest/` | `ref_generique` | 13 |
| `frontend\public\index.html` | `/favicon.ico` | `ref_generique` | 20 |
| `frontend\public\index.html` | `//assets.emergent.sh/scripts/emergent-main.js` | `ref_generique` | 26 |
| `frontend\public\index.html` | `/static/array.js` | `ref_generique` | 70 |
| `frontend\public\index.html` | `//us.i.posthog.com` | `ref_generique` | 104 |
| `frontend\README.md` | `//github.com/facebook/create-react-app` | `ref_generique` | 3 |
| `frontend\README.md` | `//localhost` | `ref_generique` | 12 |
| `frontend\README.md` | `//facebook.github.io/create-react-app/docs/running-tests` | `ref_generique` | 20 |
| `frontend\README.md` | `//facebook.github.io/create-react-app/docs/deployment` | `ref_generique` | 30 |
| `frontend\README.md` | `//facebook.github.io/create-react-app/docs/getting-started` | `ref_generique` | 44 |
| `frontend\README.md` | `//reactjs.org/` | `ref_generique` | 46 |
| `frontend\README.md` | `//facebook.github.io/create-react-app/docs/code-splitting` | `ref_generique` | 50 |
| `frontend\README.md` | `//facebook.github.io/create-react-app/docs/analyzing-the-bundle-size` | `ref_generique` | 54 |
| `frontend\README.md` | `//facebook.github.io/create-react-app/docs/making-a-progressive-web-app` | `ref_generique` | 58 |
| `frontend\README.md` | `//facebook.github.io/create-react-app/docs/advanced-configuration` | `ref_generique` | 62 |
| `frontend\README.md` | `//facebook.github.io/create-react-app/docs/troubleshooting` | `ref_generique` | 70 |
| `frontend\src\App.js` | `process.env` | `ref_generique` | 7 |
| `frontend\src\App.js` | `//emergent.sh` | `ref_generique` | 30 |
| `frontend\src\App.js` | `//avatars.githubusercontent.com/in/1201222` | `ref_generique` | 34 |
| `frontend\src\constants\testIds\index.js` | `./<feature>` | `ref_generique` | 12 |
| `frontend\src\constants\testIds\index.js` | `./auth` | `ref_generique` | 14 |
| `frontend\src\constants\testIds\index.js` | `./home` | `ref_generique` | 15 |
| `frontend\tailwind.config.js` | `./src/**/*.{js,jsx,ts,tsx}` | `ref_generique` | 5 |
| `GABRIEL_LATEX_ASSISTANT_GUIDE.md` | `//miktex.org/download` | `ref_generique` | 115 |
| `GABRIEL_LATEX_ASSISTANT_GUIDE.md` | `//arxiv.org` | `ref_generique` | 188 |
| `gabriel_repo_mapper.py` | `chemin` | `open_fichier` | 93 |
| `gabriel_repo_mapper.py` | `gabriel_repo_map.json` | `open_fichier` | 708 |
| `gabriel_repo_mapper.py` | `gabriel_repo_report.md` | `chemin_litteral` | 681 |
| `gabriel_repo_mapper.py` | `sqlite:///...` | `base_donnees` | 123 |
| `GESTION_IMAGES_3_SOLUTIONS.md` | `./images:/home/agent/app/images:ro` | `ref_generique` | 23 |
| `GESTION_IMAGES_3_SOLUTIONS.md` | `/home/agent/app/images/graphique_convergence.png` | `ref_generique` | 28 |
| `GESTION_IMAGES_3_SOLUTIONS.md` | `./images/graphique_convergence.png` | `ref_generique` | 72 |
| `GESTION_IMAGES_3_SOLUTIONS.md` | `./images/graphiques/mon_graphique.png` | `ref_generique` | 173 |
| `GESTION_IMAGES_3_SOLUTIONS.md` | `./images/graphiques/` | `ref_generique` | 224 |
| `GESTION_IMAGES_3_SOLUTIONS.md` | `./images/graphiques/convergence.png` | `ref_generique` | 230 |
| `GESTION_IMAGES_3_SOLUTIONS.md` | `./images` | `ref_generique` | 280 |
| `GESTION_IMAGES_3_SOLUTIONS.md` | `/home/agent/app/images` | `ref_generique` | 281 |
| `LATEX_ARCHITECTURE_COMPLETE.md` | `//arxiv.org` | `ref_generique` | 131 |
| `LATEX_ASSISTANT_QUICKSTART.md` | `//miktex.org/download` | `ref_generique` | 18 |
| `LATEX_ASSISTANT_QUICKSTART.md` | `//arxiv.org` | `ref_generique` | 108 |
| `memory\adaptateur_cognitif_rag.py` | `memory/dictionnaire_spectral.json` | `chemin_litteral` | 20 |
| `memory\dictionnaire_spectral.py` | `memory/dictionnaire_spectral.json` | `chemin_litteral` | 318 |
| `memory\directives_theorie_savard.md` | `//github.com/2racinede4carreunivers-dev/` | `ref_generique` | 162 |
| `memory\memoire_technique.py` | `prime_arithmetic.thy` | `chemin_litteral` | 198 |
| `memory\memoire_technique.py` | `regime_definitions.thy` | `chemin_litteral` | 211 |
| `memory\memoire_technique.py` | `gap_properties.thy` | `chemin_litteral` | 225 |
| `memory\memoire_technique.py` | `harmonie_lemmas.thy` | `chemin_litteral` | 239 |
| `memory\PRD.md` | `iteration_15.json` | `ref_generique` | 187 |
| `memory\PRD.md` | `iteration_14.json` | `ref_generique` | 200 |
| `memory\PRD.md` | `iteration_13.json` | `ref_generique` | 226 |
| `memory\PRD.md` | `iteration_12.json` | `ref_generique` | 246 |
| `memory\PRD.md` | `iteration_11.json` | `ref_generique` | 265 |
| `memory\PRD.md` | `iteration_10.json` | `ref_generique` | 303 |
| `memory\PRD.md` | `/theories` | `ref_generique` | 335 |
| `memory\PRD.md` | `/home/agent/app/theories` | `ref_generique` | 335 |
| `memory\PRD.md` | `/app/...` | `ref_generique` | 335 |
| `memory\PRD.md` | `/home/agent/app/CONFIG_ENV_GUIDE.md` | `ref_generique` | 338 |
| `memory\PRD.md` | `/home/agent/app/scripts` | `ref_generique` | 340 |
| `memory\PRD.md` | `/home/agent/app/memory` | `ref_generique` | 352 |
| `memory\PRD.md` | `/home/agent/app/data/debats-onedrive` | `ref_generique` | 373 |
| `memory\PRD.md` | `/app/agent-multiloop-Gabriel-local/` | `ref_generique` | 383 |
| `memory\PRD.md` | `emergent.sh` | `ref_generique` | 426 |
| `memory\PRD.md` | `/home/agent/app/.env` | `ref_generique` | 489 |
| `memory\PRD.md` | `./.env:/home/agent/app/.env:ro`` | `ref_generique` | 498 |
| `memory\theory_axioms_manager.py` | `Charge directives depuis memory/directives_theorie_savard.md` | `chemin_litteral` | 49 |
| `memory\theory_axioms_manager.py` | `memory/axioms.json` | `chemin_litteral` | 323 |
| `PLAN_ORGANISATION.md` | `DEMARRAGE_RAPIDE.md` | `ref_generique` | 8 |
| `PLAN_ORGANISATION.md` | `README_GUIDES.md` | `ref_generique` | 9 |
| `PLAN_ORGANISATION.md` | `README_MATHEMATICAL_v2.md` | `ref_generique` | 81 |
| `PLAN_ORGANISATION.md` | `README_FINAL.md` | `ref_generique` | 101 |
| `README.md` | `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local/actions/workflows/build.yml/badge.svg` | `ref_generique` | 3 |
| `README.md` | `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local/actions/workflows/build.yml` | `ref_generique` | 3 |
| `README.md` | `//img.shields.io/badge/License-Apache_2.0-blue.svg` | `ref_generique` | 4 |
| `README.md` | `//img.shields.io/badge/Isabelle` | `ref_generique` | 5 |
| `README.md` | `//isabelle.in.tum.de/` | `ref_generique` | 5 |
| `README.md` | `//img.shields.io/badge/Python-3.11-yellow.svg` | `ref_generique` | 6 |
| `README.md` | `//www.python.org/` | `ref_generique` | 6 |
| `README.md` | `//img.shields.io/badge/pytest-1702` | `ref_generique` | 7 |
| `README.md` | `//www.universestaucarre.com` | `ref_generique` | 124 |
| `README.md` | `//github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026.git` | `ref_generique` | 131 |
| `README.md` | `Emergent.sh` | `ref_generique` | 131 |
| `README.md` | `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local.git` | `ref_generique` | 183 |
| `RESOLUTION_ANTHROPIC_KEY_ABSENTE.md` | `/home/agent/app/.env` | `ref_generique` | 124 |
| `RESOLUTION_ANTHROPIC_KEY_ABSENTE.md` | `AUDIT_FICHIERS_ENV_COMPLET.md` | `ref_generique` | 131 |
| `SECURITY.md` | `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local/issues/new` | `ref_generique` | 89 |
| `security_validator.py` | `Valide .gitignore existe et contient .env` | `chemin_litteral` | 105 |
| `security_validator.py` | `✓ .gitignore contient .env` | `chemin_litteral` | 133 |
| `security_validator.py` | `  2. Consulter SECURITY_FIX.md` | `chemin_litteral` | 250 |
| `src\core\detecteur_asymetrique_ordonnee.py` | `utiliser comparaison_asymetrique_ordonnee.py` | `chemin_litteral` | 166 |
| `src\core\vision_gabriel.py` | `/home/agent/app/images` | `Path()` | 61 |
| `src\core\vision_gabriel.py` | `/home/agent/app/images/` | `chemin_litteral` | 120 |
| `VERIFICATION_COMPLETE_CORRECTIONS.md` | `/cygdrive/c/agent-multiloop-Gabriel-local-final/agent-multiloop-Gabriel-local/theories` | `ref_generique` | 85 |
| `VISION_GABRIEL_TOUS_FORMATS_CHEMIN.md` | `/Users/Desktop/mon_graphique.png` | `ref_generique` | 26 |
| `VISION_GABRIEL_TOUS_FORMATS_CHEMIN.md` | `./images/graphiques/convergence.png` | `ref_generique` | 32 |
| `VISION_GABRIEL_TOUS_FORMATS_CHEMIN.md` | `./images/` | `ref_generique` | 43 |
| `VISION_GABRIEL_TOUS_FORMATS_CHEMIN.md` | `./images/convergence.png` | `ref_generique` | 48 |
| `VISION_GABRIEL_TOUS_FORMATS_CHEMIN.md` | `/home/agent/app/images/convergence.png` | `ref_generique` | 52 |
| `VISION_GABRIEL_TOUS_FORMATS_CHEMIN.md` | `/Users/Philippe/Desktop/mon_graphique.png` | `ref_generique` | 93 |
| `VISION_GABRIEL_TOUS_FORMATS_CHEMIN.md` | `./images/:**` | `ref_generique` | 98 |
| `VISION_GABRIEL_TOUS_FORMATS_CHEMIN.md` | `/home/...` | `ref_generique` | 115 |
| `VISION_GABRIEL_TOUS_FORMATS_CHEMIN.md` | `./images/...` | `ref_generique` | 115 |
| `VISION_GABRIEL_TOUS_FORMATS_CHEMIN.md` | `./convergence.png?` | `ref_generique` | 124 |
| `VISION_GABRIEL_TOUS_FORMATS_CHEMIN.md` | `./images/convergence.png?` | `ref_generique` | 125 |
| `VISION_GABRIEL_TOUS_FORMATS_CHEMIN.md` | `/home/agent/app/images/...` | `ref_generique` | 235 |
| `VISION_TOUS_FORMATS_QUICKSTART.md` | `/Users/Desktop/image.png` | `ref_generique` | 13 |
| `VISION_TOUS_FORMATS_QUICKSTART.md` | `./images/photo.png` | `ref_generique` | 14 |
| `VISION_TOUS_FORMATS_QUICKSTART.md` | `./images/` | `ref_generique` | 16 |
| `VISION_TOUS_FORMATS_QUICKSTART.md` | `/home/agent/app/images/photo.png` | `ref_generique` | 17 |
| `VISION_TOUS_FORMATS_QUICKSTART.md` | `./images/graphiques/mon_graphique.png` | `ref_generique` | 54 |

## 6. Détail complet par fichier

### `.emergent\cron\applied.hash`
- **Type :** autre
- **Taille :** 0.0 o
- **Modifié :** 2026-08-03 14:07:47
- **Lignes :** 1
- **Hash MD5 :** `d41d8cd98f00`
- **Références sortantes :** *(aucune)*

### `.emergent\cron\dispatch_webhook.sh`
- **Type :** shell
- **Taille :** 2.9 Ko
- **Modifié :** 2026-08-03 14:07:47
- **Lignes :** 75
- **Hash MD5 :** `e8e3e99cd520`
- **Références sortantes (9) :**
  - ❓ `shell_appel` → `The` *(l.3)*
  - ❓ `shell_appel` → `set` *(l.4)*
  - ❓ `shell_appel` → `Fire` *(l.14)*
  - ❓ `shell_appel` → `if` *(l.15)*
  - ❓ `shell_appel` → `Stop` *(l.24)*
  - ❓ `shell_appel` → `v` *(l.34)*
  - ❓ `shell_appel` → `read_secret` *(l.43)*
  - ❓ `shell_appel` → `RUN_ID` *(l.53)*
  - ❓ `shell_appel` → `HTTP_STATUS` *(l.61)*

### `.emergent\cron\watch_crons.sh`
- **Type :** shell
- **Taille :** 1.3 Ko
- **Modifié :** 2026-08-03 14:07:47
- **Lignes :** 38
- **Hash MD5 :** `19105239f77c`
- **Références sortantes (4) :**
  - ❓ `shell_appel` → `It` *(l.5)*
  - ❓ `shell_appel` → `set` *(l.6)*
  - ❓ `shell_appel` → `hash_file` *(l.14)*
  - ❓ `shell_appel` → `curl` *(l.31)*

### `.emergent\cron\webhook-crons`
- **Type :** autre
- **Taille :** 475.0 o
- **Modifié :** 2026-08-03 14:07:47
- **Lignes :** 9
- **Hash MD5 :** `445393fab656`
- **Références sortantes :** *(aucune)*

### `.emergent\cron\webhook_crond.sh`
- **Type :** shell
- **Taille :** 1.8 Ko
- **Modifié :** 2026-08-03 14:07:47
- **Lignes :** 47
- **Hash MD5 :** `8f6abec4e3f2`
- **Références sortantes (4) :**
  - ❓ `shell_appel` → `Before` *(l.5)*
  - ❓ `shell_appel` → `set` *(l.8)*
  - ❓ `shell_appel` → `if` *(l.17)*
  - ❓ `shell_appel` → `Debian` *(l.27)*

### `.emergent\emergent.yml`
- **Type :** yaml
- **Taille :** 203.0 o
- **Modifié :** 2026-08-15 00:15:16
- **Lignes :** 6
- **Hash MD5 :** `da3ae77df427`
- **Références sortantes :** *(aucune)*

### `.emergent\summary.txt`
- **Type :** texte
- **Taille :** 91.0 Ko
- **Modifié :** 2026-08-03 14:07:47
- **Lignes :** 2446
- **Hash MD5 :** `a43d8df2621a`
- **Références sortantes (19) :**
  - ❓ `ref_generique` → `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local` *(l.36)*
  - ✅ `ref_generique` → `SECURITY.md` *(l.128)*
  - ✅ `ref_generique` → `CONTRIBUTING.md` *(l.128)*
  - ✅ `ref_generique` → `CHANGELOG.md` *(l.128)*
  - ✅ `ref_generique` → `declaration_securite.md` *(l.128)*
  - ✅ `ref_generique` → `.github\workflows\build.yml` *(l.296)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.399)*
  - ❓ `ref_generique` → `emrgent.sh` *(l.586)*
  - ❓ `ref_generique` → `/dist/` *(l.750)*
  - ❓ `ref_generique` → `./theories/methode_spectral.thy` *(l.1009)*
  - ❓ `ref_generique` → `./theories/methode_spectral.thy`` *(l.1013)*
  - ❓ `ref_generique` → `attestation_report.txt` *(l.1031)*
  - ❓ `ref_generique` → `XXX.thy` *(l.1033)*
  - ❓ `ref_generique` → `./XXX` *(l.1034)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\core\pipeline.py` *(l.1081)*
  - ❓ `ref_generique` → `SHA256SUMS.txt` *(l.1151)*
  - ❓ `ref_generique` → `Methode_spectral.thy` *(l.1291)*
  - ❓ `ref_generique` → `emergent.sh` *(l.1339)*
  - ✅ `ref_generique` → `README.md` *(l.2084)*

### `.emergent\system_deps.txt`
- **Type :** texte
- **Taille :** 17.0 o
- **Modifié :** 2026-08-03 14:07:47
- **Lignes :** 2
- **Hash MD5 :** `724fa7b62437`
- **Références sortantes :** *(aucune)*

### `.gitconfig`
- **Type :** autre
- **Taille :** 64.0 o
- **Modifié :** 2026-08-03 14:07:47
- **Lignes :** 4
- **Hash MD5 :** `afb33b54b84a`
- **Références sortantes :** *(aucune)*

### `.github\workflows\build.yml`
- **Type :** yaml
- **Taille :** 4.1 Ko
- **Modifié :** 2026-08-03 14:07:47
- **Lignes :** 117
- **Hash MD5 :** `6975046b7121`
- **Références sortantes :** *(aucune)*

### `.github\workflows\codacy.yml`
- **Type :** yaml
- **Taille :** 2.5 Ko
- **Modifié :** 2026-08-03 14:07:47
- **Lignes :** 62
- **Hash MD5 :** `a058ff3ec187`
- **Références sortantes :** *(aucune)*

### `.gitignore`
- **Type :** autre
- **Taille :** 5.5 Ko
- **Modifié :** 2026-08-15 00:15:16
- **Lignes :** 276
- **Hash MD5 :** `52567df68c0f`
- **Références sortantes :** *(aucune)*

### `ANALYSE_GITHUB_SYNC_FEASIBILITY.md`
- **Type :** markdown
- **Taille :** 19.9 Ko
- **Modifié :** 2026-08-03 14:07:47
- **Lignes :** 641
- **Hash MD5 :** `8f076a26cd42`
- **Références sortantes (19) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.32)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\geometrie_spectre_premier.thy` *(l.33)*
  - ❓ `ref_generique` → `chaos_harmonic_discrete.thy` *(l.34)*
  - ❓ `ref_generique` → `universes_carre.thy` *(l.35)*
  - ❓ `ref_generique` → `/data/theories` *(l.103)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\memory\__init__.py` *(l.150)*
  - ❓ `ref_generique` → `github_client.py` *(l.151)*
  - ❓ `ref_generique` → `git_sync_service.py` *(l.152)*
  - ❓ `ref_generique` → `conflict_resolver.py` *(l.153)*
  - ❓ `ref_generique` → `token_manager.py` *(l.154)*
  - ❓ `ref_generique` → `file_contents.sh` *(l.271)*
  - ❓ `ref_generique` → `gabriel-deployment.yaml` *(l.301)*
  - ❓ `ref_generique` → `sync-configmap.yaml` *(l.302)*
  - ❓ `ref_generique` → `github-secret.yaml` *(l.303)*
  - ❓ `ref_generique` → `services.yaml` *(l.304)*
  - ❓ `ref_generique` → `/cache/hol` *(l.335)*
  - ❓ `ref_generique` → `//github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026.git` *(l.409)*
  - ❓ `ref_generique` → `fichier.thy` *(l.427)*
  - ❓ `ref_generique` → `Emergent.sh` *(l.431)*

### `ANALYSE_HOL_UNIFIEE_PROFONDE.md`
- **Type :** markdown
- **Taille :** 11.3 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 296
- **Hash MD5 :** `5a501fb518b3`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\validation_hol_unifiee.thy` *(l.284)*

### `ANALYSE_RAPPORT_SESSION_GABRIEL_DISCRIMINATION.md`
- **Type :** markdown
- **Taille :** 16.1 Ko
- **Modifié :** 2026-08-03 14:07:47
- **Lignes :** 394
- **Hash MD5 :** `04406a4a113c`
- **Références sortantes (2) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.40)*
  - ❓ `ref_generique` → `gabriel_multiloop.py` *(l.215)*

### `APPLY_THEORETICAL_PATTERNS_MANUALLY.txt`
- **Type :** texte
- **Taille :** 4.2 Ko
- **Modifié :** 2026-08-03 14:07:47
- **Lignes :** 107
- **Hash MD5 :** `f160e650434a`
- **Références sortantes :** *(aucune)*

### `AUTHORS`
- **Type :** autre
- **Taille :** 6.1 Ko
- **Modifié :** 2026-08-03 14:07:47
- **Lignes :** 128
- **Hash MD5 :** `2cfa4405519f`
- **Références sortantes :** *(aucune)*

### `BADGE_QUICKSTART.md`
- **Type :** markdown
- **Taille :** 3.6 Ko
- **Modifié :** 2026-08-03 14:07:47
- **Lignes :** 82
- **Hash MD5 :** `73a94fc094c9`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main.py` *(l.11)*

### `BADGE_SCIENTIFIQUE_IMPLEMENTATION.md`
- **Type :** markdown
- **Taille :** 9.5 Ko
- **Modifié :** 2026-08-03 14:07:47
- **Lignes :** 192
- **Hash MD5 :** `224cd19a18f3`
- **Références sortantes (2) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main.py` *(l.5)*
  - ❓ `ref_generique` → `/app/logs/agent_cli.log` *(l.153)*

### `BILAN_COMPLET_SESSION.md`
- **Type :** markdown
- **Taille :** 9.5 Ko
- **Modifié :** 2026-08-03 14:07:47
- **Lignes :** 286
- **Hash MD5 :** `9b49fb4e75a0`
- **Références sortantes (13) :**
  - ✅ `ref_generique` → `CORRECTION_GABRIEL_COMPARAISON_ASYMETRIQUE.md` *(l.31)*
  - ✅ `ref_generique` → `SOLUTION_INCOH_GABRIEL.md` *(l.32)*
  - ✅ `ref_generique` → `RAPPORT_FINAL_CORRECTION.txt` *(l.33)*
  - ✅ `ref_generique` → `DIAGNOSTIC_LLM_CONFLICT_OPENAI_ANTHROPIC.md` *(l.61)*
  - ✅ `ref_generique` → `REPONSE_TA_QUESTION_OPENAI_BLOQUE_ANTHROPIC.md` *(l.62)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docker-compose.yml` *(l.88)*
  - ❓ `ref_generique` → `AUDIT_FICHIERS_ENV_COMPLET.md` *(l.94)*
  - ✅ `ref_generique` → `RESOLUTION_ANTHROPIC_KEY_ABSENTE.md` *(l.95)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\env.example.txt` *(l.108)*
  - ❓ `ref_generique` → `RESOLUTION_ENV_ABSENT_AU_LANCEMENT.md` *(l.122)*
  - ✅ `ref_generique` → `TEST_CORRECTION_GABRIEL.py` *(l.141)*
  - ✅ `ref_generique` → `RESUME_COMPLET_CORRECTION.md` *(l.150)*
  - ✅ `ref_generique` → `DEPLOYMENT_STATUS.txt` *(l.156)*

### `CHANGELOG.md`
- **Type :** markdown
- **Taille :** 8.0 Ko
- **Modifié :** 2026-08-03 14:07:47
- **Lignes :** 227
- **Hash MD5 :** `14ebb68c3e95`
- **Références sortantes (4) :**
  - ❓ `ref_generique` → `//keepachangelog.com/fr/1.1.0/` *(l.5)*
  - ❓ `ref_generique` → `//semver.org/lang/fr/` *(l.6)*
  - ❓ `ref_generique` → `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local` *(l.9)*
  - ✅ `ref_generique` → `CONTRIBUTING.md` *(l.226)*

### `CONTRIBUTING.md`
- **Type :** markdown
- **Taille :** 14.1 Ko
- **Modifié :** 2026-08-03 14:07:47
- **Lignes :** 361
- **Hash MD5 :** `2aec6ff82996`
- **Références sortantes (10) :**
  - ❓ `ref_generique` → `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local.git` *(l.74)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\requirements.txt` *(l.79)*
  - ❓ `ref_generique` → `//isabelle.in.tum.de/website-Isabelle2025-2/installation.html` *(l.86)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\core\spectral_core.py` *(l.165)*
  - ✅ `ref_generique` → `CHANGELOG.md` *(l.213)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\scripts\isabelle_static_check.py` *(l.295)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\tests\test_section_XI_XII_integration.py` *(l.295)*
  - ✅ `ref_generique` → `SECURITY.md` *(l.350)*
  - ✅ `ref_generique` → `declaration_securite.md` *(l.350)*
  - ✅ `ref_generique` → `AUTHORS` *(l.358)*

### `CORRECTIONS_APPLIQUEES_CONFIRMATION.md`
- **Type :** markdown
- **Taille :** 3.0 Ko
- **Modifié :** 2026-08-03 14:07:47
- **Lignes :** 102
- **Hash MD5 :** `681dea177224`
- **Références sortantes (2) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.2)*
  - ❓ `ref_generique` → `/cygdrive/c/agent-multiloop-Gabriel-local-final/agent-multiloop-Gabriel-local/theories` *(l.93)*

### `CORRECTIONS_DEFINITIVES_LIGNES_2595_2915.md`
- **Type :** markdown
- **Taille :** 9.4 Ko
- **Modifié :** 2026-08-03 14:07:47
- **Lignes :** 283
- **Hash MD5 :** `901d6631cbcf`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.2)*

### `CORRECTION_DEFINITIVE_LIGNE_2605.md`
- **Type :** markdown
- **Taille :** 2.6 Ko
- **Modifié :** 2026-08-03 14:07:47
- **Lignes :** 86
- **Hash MD5 :** `03ad8b37acd4`
- **Références sortantes (1) :**
  - ❓ `ref_generique` → `/cygdrive/c/agent-multiloop-Gabriel-local-final/agent-multiloop-Gabriel-local/theories` *(l.75)*

### `CORRECTION_FINAL_RsP_k.thy`
- **Type :** isabelle
- **Taille :** 6.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 178
- **Hash MD5 :** `15dc73595881`
- **Références sortantes :** *(aucune)*

### `CORRECTION_GABRIEL_COMPARAISON_ASYMETRIQUE.md`
- **Type :** markdown
- **Taille :** 3.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 136
- **Hash MD5 :** `d3032fb7bd59`
- **Références sortantes :** *(aucune)*

### `CORRECTION_GABRIEL_COMPARAISON_RESUME.txt`
- **Type :** texte
- **Taille :** 4.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 161
- **Hash MD5 :** `67b5cf543bcf`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` *(l.148)*

### `CORRECTION_THEOREM_RsP_k.thy`
- **Type :** isabelle
- **Taille :** 4.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 122
- **Hash MD5 :** `a0a2f0f3bdf1`
- **Références sortantes :** *(aucune)*

### `DEPLOYMENT_STATUS.txt`
- **Type :** texte
- **Taille :** 5.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 129
- **Hash MD5 :** `140614baf653`
- **Références sortantes :** *(aucune)*

### `DIAGNOSTIC_LLM_CONFLICT_OPENAI_ANTHROPIC.md`
- **Type :** markdown
- **Taille :** 12.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 375
- **Hash MD5 :** `f534c64d4b47`
- **Références sortantes (3) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\config.yaml` *(l.16)*
  - ❓ `ref_generique` → `test_llm_routing.py` *(l.270)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` *(l.346)*

### `GABRIEL_COGNITIVE_INTEGRATION.md`
- **Type :** markdown
- **Taille :** 10.9 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 281
- **Hash MD5 :** `d02be104fe22`
- **Références sortantes (2) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.7)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\validation_hol_unifiee.thy` *(l.202)*

### `GABRIEL_LATEX_ASSISTANT_GUIDE.md`
- **Type :** markdown
- **Taille :** 10.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 373
- **Hash MD5 :** `457c8f79d29f`
- **Références sortantes (2) :**
  - ❓ `ref_generique` → `//miktex.org/download` *(l.115)*
  - ❓ `ref_generique` → `//arxiv.org` *(l.188)*

### `GABRIEL_v7_SYSTEME_MEMOIRE.md`
- **Type :** markdown
- **Taille :** 14.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 440
- **Hash MD5 :** `2737a2e9baae`
- **Références sortantes (5) :**
  - ✅ `ref_generique` → `memory\memoire_conceptuelle.py` *(l.70)*
  - ✅ `ref_generique` → `memory\memoire_technique.py` *(l.74)*
  - ✅ `ref_generique` → `memory\gestionnaire_erreurs.py` *(l.78)*
  - ✅ `ref_generique` → `memory\error_cache\errors.json` *(l.83)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` *(l.86)*

### `GESTION_IMAGES_3_SOLUTIONS.md`
- **Type :** markdown
- **Taille :** 8.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 319
- **Hash MD5 :** `7f8726d355d2`
- **Références sortantes (10) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docker-compose.yml` *(l.12)*
  - ❓ `ref_generique` → `./images:/home/agent/app/images:ro` *(l.23)*
  - ❓ `ref_generique` → `/home/agent/app/images/graphique_convergence.png` *(l.28)*
  - ❓ `ref_generique` → `./images/graphique_convergence.png` *(l.72)*
  - ❓ `ref_generique` → `./images/graphiques/mon_graphique.png` *(l.173)*
  - ❓ `ref_generique` → `./images/graphiques/` *(l.224)*
  - ❓ `ref_generique` → `./images/graphiques/convergence.png` *(l.230)*
  - ❓ `ref_generique` → `./images` *(l.280)*
  - ❓ `ref_generique` → `/home/agent/app/images` *(l.281)*
  - ✅ `ref_generique` → `src\core\vision_gabriel.py` *(l.318)*

### `GUIDE_CORRECTION_THEOREM_RsP_k.md`
- **Type :** markdown
- **Taille :** 9.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 244
- **Hash MD5 :** `b9afdc919b4d`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.2)*

### `LATEX_ARCHITECTURE_COMPLETE.md`
- **Type :** markdown
- **Taille :** 11.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 250
- **Hash MD5 :** `4a895e19d765`
- **Références sortantes (1) :**
  - ❓ `ref_generique` → `//arxiv.org` *(l.131)*

### `LATEX_ASSISTANT_QUICKSTART.md`
- **Type :** markdown
- **Taille :** 5.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 164
- **Hash MD5 :** `c70b55bd90fa`
- **Références sortantes (2) :**
  - ❓ `ref_generique` → `//miktex.org/download` *(l.18)*
  - ❓ `ref_generique` → `//arxiv.org` *(l.108)*

### `MEMOIRE_v7_INSTALLATION_COMPLETE.txt`
- **Type :** texte
- **Taille :** 2.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 75
- **Hash MD5 :** `5c7241783d6d`
- **Références sortantes (6) :**
  - ✅ `ref_generique` → `memory\memoire_conceptuelle.py` *(l.8)*
  - ✅ `ref_generique` → `memory\memoire_technique.py` *(l.9)*
  - ✅ `ref_generique` → `memory\gestionnaire_erreurs.py` *(l.10)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\memory\__init__.py` *(l.12)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` *(l.15)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\core\llm_manager.py` *(l.16)*

### `METAPHORES_GEOMETRIQUES_GUIDE.md`
- **Type :** markdown
- **Taille :** 11.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 343
- **Hash MD5 :** `7eeb6b494de3`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` *(l.303)*

### `METAPHORES_GEOMETRIQUES_QUICKSTART.md`
- **Type :** markdown
- **Taille :** 3.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 89
- **Hash MD5 :** `f1d2f2f0467b`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` *(l.15)*

### `PLAN_ORGANISATION.md`
- **Type :** markdown
- **Taille :** 6.3 Ko
- **Modifié :** 2026-08-15 08:16:56
- **Lignes :** 167
- **Hash MD5 :** `d23bf8e73d0a`
- **Références sortantes (82) :**
  - ❓ `ref_generique` → `DEMARRAGE_RAPIDE.md` *(l.8)*
  - ❓ `ref_generique` → `README_GUIDES.md` *(l.9)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GO_QUICK_START.md` *(l.15)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\REPONSE_RAPIDE_RECONSTRUCTION.md` *(l.16)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\QUICK_START_5_MINUTES.md` *(l.17)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\QUICK_START_IMAGE_ANALYSIS.md` *(l.18)*
  - ✅ `ref_generique` → `README.md` *(l.19)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md` *(l.22)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_IMAGE_ANALYSIS_COMPLETE_GUIDE.md` *(l.23)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\IMAGE_ANALYSIS_ANSWER_DIRECT.md` *(l.24)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GUIDE_ANALYSE_AVEC_CRITERES.md` *(l.25)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\COMMANDES_PRATIQUES_ANALYSE.md` *(l.26)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GUIDE_RECONSTRUCTION_REDEMARRAGE.md` *(l.30)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\FINAL_RECONSTRUCTION_SUMMARY.txt` *(l.31)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\VALIDATION_HOL_UNIFIEE_ANALYSIS.md` *(l.35)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\VALIDATION_HOL_INTEGRATION_COMPLETE.md` *(l.36)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_VISION_QUICK_START.md` *(l.40)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` *(l.41)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_VISION_VERIFICATION_COMPLETE.md` *(l.42)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_COMPLETE_VISION_INTEGRATION.md` *(l.43)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CINEMATIC_DEPLOYMENT.md` *(l.47)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\DEPLOYMENT_CHECKLIST_v4.0.md` *(l.48)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\DEPLOYMENT_SUMMARY.md` *(l.49)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v5.4_WORKING_SOLUTION.md` *(l.50)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CONFIG_ENV_GUIDE.md` *(l.54)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` *(l.55)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\UTF8_ENCODING_FIX.md` *(l.56)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GUIDE_JEDIT_GABRIEL.md` *(l.60)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\POWERSHELL_ISE_GUIDE.md` *(l.61)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\JEDIT_QUICK_REFERENCE.md` *(l.62)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\SHORTCUTS_AND_TIPS.md` *(l.63)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PYTEST_CHECKLIST.md` *(l.67)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PYTEST_EXECUTION_GUIDE.md` *(l.68)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PYTEST_INDEX.md` *(l.69)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PYTEST_LIST_COMPLETE.md` *(l.70)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PYTEST_SUMMARY.md` *(l.71)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\COMMANDS_COMPLETE_REFERENCE.md` *(l.75)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\QUICK_REFERENCE.md` *(l.76)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\guide_utilisateur\01_DEMARRAGE_RAPIDE\INDEX.md` *(l.77)*
  - ❓ `ref_generique` → `README_MATHEMATICAL_v2.md` *(l.81)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CORRECTION_RSA_v2.2.md` *(l.83)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\SYNTHESE_RSA_v2.2.md` *(l.84)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\SYNTHESE_ULTIME_v2.1.md` *(l.85)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\HOL_ISABELLE_FIX.md` *(l.86)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\HOL4_SYSTEMATIC_PROOFS.md` *(l.87)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\BUG_FIX_URGENT_HOL.md` *(l.88)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v2.1_RELEASE_NOTES.md` *(l.92)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v2.2_RSA_CAPABILITY.md` *(l.93)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v3.0_MULTILOOP_VALIDATION.md` *(l.94)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v4.0_THEORY_MEMORY.md` *(l.95)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v5.0_LLM_ROUTING.md` *(l.96)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v5.1_SAFE_BUDGET.md` *(l.97)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v5.2_DEPLOYMENT_SUMMARY.md` *(l.98)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v5.2_HOL_FORMAL.md` *(l.99)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v5_UPDATE_GUIDE.md` *(l.100)*
  - ❓ `ref_generique` → `README_FINAL.md` *(l.101)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` *(l.102)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md` *(l.103)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CINEMATIC_INTEGRATION_GUIDE.md` *(l.107)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CINEMATIC_MODE_SUMMARY.md` *(l.108)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_DOMAIN_SYSTEM_INTEGRATION_GUIDE.md` *(l.109)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_PARAMETRIC_VALIDATION_GUIDE.md` *(l.110)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_PRODUCTION_VALIDATION_GUIDE.md` *(l.111)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\INTEGRATION_UNIVERSESTAUCARRE.md` *(l.112)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\MIGRATION_VALIDATION_SYSTEMS.md` *(l.113)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PATCH_THEORETICAL_RECOGNITION.md` *(l.114)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_PERFORMANCE_OPTIMIZATION.md` *(l.118)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_PORT_FIX_v5.3.md` *(l.119)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_FINAL_v5_SOCKET_CLEANUP.md` *(l.120)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PORT_CLEANUP_IMPLEMENTATION.md` *(l.121)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_DEBUGGER_PAUSE_STATUS.md` *(l.125)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CLAUDE_BUDGET_GUIDE.md` *(l.126)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\OPTIMIZATION_SUMMARY.md` *(l.127)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\MULTIFORMAT_TEMPLATES_GUIDE.md` *(l.129)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\FINAL_300_TEMPLATES_SUMMARY.md` *(l.130)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PROJECTS_TEMPLATES_GUIDE.md` *(l.131)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\TEMPLATES_SUMMARY.md` *(l.132)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\FILES_v5.0.md` *(l.133)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CHECKLIST_FINAL.md` *(l.134)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\TODO_ANALYSE.md` *(l.135)*
  - ✅ `ref_generique` → `CHANGELOG.md` *(l.136)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\REPONSE_OUI_PREUVES_HOL4_SYSTEMATIQUES.md` *(l.137)*

### `PLAN_TRIFOCAL_GUIDE_COMPLET.md`
- **Type :** markdown
- **Taille :** 11.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 336
- **Hash MD5 :** `5535fb7e37f3`
- **Références sortantes (2) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.253)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\ui\cli.py` *(l.253)*

### `PLAN_TRIFOCAL_IMAGE_ACCESS.md`
- **Type :** markdown
- **Taille :** 5.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 139
- **Hash MD5 :** `991247d81c05`
- **Références sortantes (2) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.57)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\ui\cli.py` *(l.57)*

### `PLAN_TRIFOCAL_QUICKSTART.md`
- **Type :** markdown
- **Taille :** 3.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 96
- **Hash MD5 :** `8e908f21bf9c`
- **Références sortantes :** *(aucune)*

### `RAPPORT_FINAL_CORRECTION.txt`
- **Type :** texte
- **Taille :** 7.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 202
- **Hash MD5 :** `e28d3e41b75c`
- **Références sortantes (5) :**
  - ✅ `ref_generique` → `CORRECTION_GABRIEL_COMPARAISON_ASYMETRIQUE.md` *(l.56)*
  - ✅ `ref_generique` → `SOLUTION_INCOH_GABRIEL.md` *(l.57)*
  - ✅ `ref_generique` → `CORRECTION_GABRIEL_COMPARAISON_RESUME.txt` *(l.58)*
  - ✅ `ref_generique` → `src\core\integrateur_memoire_patch.py` *(l.146)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` *(l.177)*

### `README.md`
- **Type :** markdown
- **Taille :** 16.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 265
- **Hash MD5 :** `249d1b0d9f49`
- **Références sortantes (12) :**
  - ❓ `ref_generique` → `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local/actions/workflows/build.yml/badge.svg` *(l.3)*
  - ❓ `ref_generique` → `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local/actions/workflows/build.yml` *(l.3)*
  - ❓ `ref_generique` → `//img.shields.io/badge/License-Apache_2.0-blue.svg` *(l.4)*
  - ❓ `ref_generique` → `//img.shields.io/badge/Isabelle` *(l.5)*
  - ❓ `ref_generique` → `//isabelle.in.tum.de/` *(l.5)*
  - ❓ `ref_generique` → `//img.shields.io/badge/Python-3.11-yellow.svg` *(l.6)*
  - ❓ `ref_generique` → `//www.python.org/` *(l.6)*
  - ❓ `ref_generique` → `//img.shields.io/badge/pytest-1702` *(l.7)*
  - ❓ `ref_generique` → `//www.universestaucarre.com` *(l.124)*
  - ❓ `ref_generique` → `//github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026.git` *(l.131)*
  - ❓ `ref_generique` → `Emergent.sh` *(l.131)*
  - ❓ `ref_generique` → `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local.git` *(l.183)*

### `RELEASE_NOTES_v3.35.md`
- **Type :** markdown
- **Taille :** 12.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 102
- **Hash MD5 :** `d33b739dc380`
- **Références sortantes :** *(aucune)*

### `REPONSE_TA_QUESTION_OPENAI_BLOQUE_ANTHROPIC.md`
- **Type :** markdown
- **Taille :** 8.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 267
- **Hash MD5 :** `5bc5995e41b6`
- **Références sortantes (3) :**
  - ✅ `ref_generique` → `DIAGNOSTIC_LLM_CONFLICT_OPENAI_ANTHROPIC.md` *(l.241)*
  - ✅ `ref_generique` → `src\core\llm_router_explicite.py` *(l.246)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` *(l.247)*

### `RESOLUTION_ANTHROPIC_KEY_ABSENTE.md`
- **Type :** markdown
- **Taille :** 9.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 256
- **Hash MD5 :** `db6fe599cd4b`
- **Références sortantes (4) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docker-compose.yml` *(l.6)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\config.yaml` *(l.33)*
  - ❓ `ref_generique` → `/home/agent/app/.env` *(l.124)*
  - ❓ `ref_generique` → `AUDIT_FICHIERS_ENV_COMPLET.md` *(l.131)*

### `RESUME_COMPLET_CORRECTION.md`
- **Type :** markdown
- **Taille :** 8.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 207
- **Hash MD5 :** `6b20343f52a3`
- **Références sortantes (3) :**
  - ✅ `ref_generique` → `src\core\detecteur_asymetrique_ordonnee.py` *(l.32)*
  - ✅ `ref_generique` → `memory\comparaison_asymetrique_ordonnee.py` *(l.38)*
  - ✅ `ref_generique` → `src\core\gabriel_comparaison_asymetrique.py` *(l.44)*

### `SCHEMAS_FIGURES_VISION_GUIDE.md`
- **Type :** markdown
- **Taille :** 10.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 346
- **Hash MD5 :** `522e5b3bb6fe`
- **Références sortantes (3) :**
  - ✅ `ref_generique` → `src\core\generateur_schemas_avances.py` *(l.312)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` *(l.313)*
  - ✅ `ref_generique` → `src\core\vision_gabriel.py` *(l.317)*

### `SCHEMAS_VISION_QUICKSTART.md`
- **Type :** markdown
- **Taille :** 2.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 91
- **Hash MD5 :** `6e4a860c1286`
- **Références sortantes (2) :**
  - ✅ `ref_generique` → `src\core\generateur_schemas_avances.py` *(l.18)*
  - ✅ `ref_generique` → `src\core\vision_gabriel.py` *(l.27)*

### `SECURITY.md`
- **Type :** markdown
- **Taille :** 8.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 197
- **Hash MD5 :** `8576728e4a24`
- **Références sortantes (2) :**
  - ✅ `ref_generique` → `declaration_securite.md` *(l.3)*
  - ❓ `ref_generique` → `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local/issues/new` *(l.89)*

### `SOLUTION_DEFINITIVE_RsP_k.md`
- **Type :** markdown
- **Taille :** 7.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 226
- **Hash MD5 :** `0e8036ae0e88`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.206)*

### `SOLUTION_INCOH_GABRIEL.md`
- **Type :** markdown
- **Taille :** 3.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 151
- **Hash MD5 :** `09301b3e962a`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `memory\comparaison_asymetrique_ordonnee.py` *(l.26)*

### `TEST_CORRECTION_GABRIEL.py`
- **Type :** python
- **Taille :** 8.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 234
- **Hash MD5 :** `2443ffa512b6`
- **Références sortantes (6) :**
  - ❓ `import_module` → `sys` *(l.13)*
  - ❓ `import_module` → `pathlib` *(l.15)*
  - ✅ `import_module` → `src\core\detecteur_asymetrique_ordonnee.py` *(l.19)*
  - ✅ `import_module` → `src\core\gabriel_comparaison_asymetrique.py` *(l.21)*
  - ✅ `import_module` → `memory\comparaison_asymetrique_ordonnee.py` *(l.22)*
  - ❓ `import_module` → `traceback` *(l.228)*

### `VERIFICATION_COMPLETE_CORRECTIONS.md`
- **Type :** markdown
- **Taille :** 3.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 115
- **Hash MD5 :** `267b5789049b`
- **Références sortantes (2) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.4)*
  - ❓ `ref_generique` → `/cygdrive/c/agent-multiloop-Gabriel-local-final/agent-multiloop-Gabriel-local/theories` *(l.85)*

### `VISION_GABRIEL_TOUS_FORMATS_CHEMIN.md`
- **Type :** markdown
- **Taille :** 8.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 251
- **Hash MD5 :** `aceafb47cf16`
- **Références sortantes (15) :**
  - ✅ `ref_generique` → `src\core\vision_gabriel.py` *(l.4)*
  - ❓ `ref_generique` → `/Users/Desktop/mon_graphique.png` *(l.26)*
  - ❓ `ref_generique` → `./images/graphiques/convergence.png` *(l.32)*
  - ❓ `ref_generique` → `./images/` *(l.43)*
  - ❓ `ref_generique` → `./images/convergence.png` *(l.48)*
  - ❓ `ref_generique` → `/home/agent/app/images/convergence.png` *(l.52)*
  - ❓ `ref_generique` → `/Users/Philippe/Desktop/mon_graphique.png` *(l.93)*
  - ❓ `ref_generique` → `./images/:**` *(l.98)*
  - ❓ `ref_generique` → `/home/...` *(l.115)*
  - ❓ `ref_generique` → `./images/...` *(l.115)*
  - ✅ `ref_generique` → `.` *(l.116)*
  - ❓ `ref_generique` → `./convergence.png?` *(l.124)*
  - ❓ `ref_generique` → `./images/convergence.png?` *(l.125)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docker-compose.yml` *(l.157)*
  - ❓ `ref_generique` → `/home/agent/app/images/...` *(l.235)*

### `VISION_TOUS_FORMATS_QUICKSTART.md`
- **Type :** markdown
- **Taille :** 2.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 85
- **Hash MD5 :** `f3550ee1e56c`
- **Références sortantes (6) :**
  - ✅ `ref_generique` → `src\core\vision_gabriel.py` *(l.4)*
  - ❓ `ref_generique` → `/Users/Desktop/image.png` *(l.13)*
  - ❓ `ref_generique` → `./images/photo.png` *(l.14)*
  - ❓ `ref_generique` → `./images/` *(l.16)*
  - ❓ `ref_generique` → `/home/agent/app/images/photo.png` *(l.17)*
  - ❓ `ref_generique` → `./images/graphiques/mon_graphique.png` *(l.54)*

### `activation_memoire.py`
- **Type :** python
- **Taille :** 4.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 136
- **Hash MD5 :** `47f033fd81ef`
- **Références sortantes (10) :**
  - ❓ `import_module` → `sys` *(l.6)*
  - ❓ `import_module` → `pathlib` *(l.8)*
  - ✅ `Path()` → `memory` *(l.18)*
  - ✅ `Path()` → `agent-multiloop-Gabriel-local\src\core\llm_manager.py` *(l.44)*
  - ✅ `Path()` → `src\core\integrateur_memoire.py` *(l.59)*
  - ✅ `chemin_litteral` → `memory\memoire_conceptuelle.py` *(l.20)*
  - ✅ `chemin_litteral` → `memory\memoire_technique.py` *(l.21)*
  - ✅ `chemin_litteral` → `memory\gestionnaire_erreurs.py` *(l.22)*
  - ❓ `chemin_litteral` → `error_cache/errors.json` *(l.23)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\memory\__init__.py` *(l.24)*

### `agent-multiloop-Gabriel-local\.dockerignore`
- **Type :** autre
- **Taille :** 3.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 146
- **Hash MD5 :** `3387aa85e14d`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\.github\workflows\build.yml`
- **Type :** yaml
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 39
- **Hash MD5 :** `d6544701b499`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\.github\workflows\tests.yml`
- **Type :** yaml
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 50
- **Hash MD5 :** `aa9189c33a11`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\.gitignore`
- **Type :** autre
- **Taille :** 1.8 Ko
- **Modifié :** 2026-08-15 00:15:16
- **Lignes :** 104
- **Hash MD5 :** `4ff69d74f201`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\00_START_HERE_IMAGE_ANALYSIS.md`
- **Type :** markdown
- **Taille :** 15.3 Ko
- **Modifié :** 2026-08-16 20:14:32
- **Lignes :** 384
- **Hash MD5 :** `343e7832adfc`
- **Références sortantes (7) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\gabriel_vision_integration.py` *(l.25)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\COMPLETE_INTEGRATION_INSTRUCTIONS.md` *(l.26)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\INTEGRATION_PATCH_IMAGE_ANALYSIS.md` *(l.50)*
  - ❓ `ref_generique` → `/home/.../image.png` *(l.151)*
  - ❓ `ref_generique` → `./images/figure.png` *(l.152)*
  - ❓ `ref_generique` → `./test.png` *(l.305)*
  - ❓ `ref_generique` → `/nonexistent/image.png` *(l.313)*

### `agent-multiloop-Gabriel-local\BUG_FIX_URGENT_HOL.md`
- **Type :** markdown
- **Taille :** 5.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 241
- **Hash MD5 :** `03afa4491092`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\CHANGELOG.md`
- **Type :** markdown
- **Taille :** 4.5 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 194
- **Hash MD5 :** `f4e31ffb1cd0`
- **Références sortantes (2) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.102)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docker-compose.yml` *(l.140)*

### `agent-multiloop-Gabriel-local\CHECKLIST_FINAL.md`
- **Type :** markdown
- **Taille :** 10.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 390
- **Hash MD5 :** `d79835ff3021`
- **Références sortantes (19) :**
  - ❓ `ref_generique` → `os.env` *(l.86)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\mathematical_engine.py` *(l.111)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\hol_lean_interface.py` *(l.112)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\pdf_rag_processor.py` *(l.113)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\memory\__init__.py` *(l.114)*
  - ❓ `ref_generique` → `riemann_spectral.thy` *(l.117)*
  - ❓ `ref_generique` → `pdf_index.json` *(l.125)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\gabriel_mathematical.py` *(l.127)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\integration_mathematical.py` *(l.128)*
  - ❓ `ref_generique` → `config_mathematical.env` *(l.129)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\requirements.txt` *(l.130)*
  - ❓ `ref_generique` → `README_MATHEMATICAL_v2.md` *(l.132)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` *(l.133)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CHECKLIST_FINAL.md` *(l.134)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main.py` *(l.136)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.137)*
  - ✅ `ref_generique` → `backend\server.py` *(l.141)*
  - ❓ `ref_generique` → `/api/query` *(l.197)*
  - ❓ `ref_generique` → `//raw.githubusercontent.com/leanprover/elan/master/elan-init.sh` *(l.299)*

### `agent-multiloop-Gabriel-local\CINEMATIC_DEPLOYMENT.md`
- **Type :** markdown
- **Taille :** 8.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 302
- **Hash MD5 :** `e04e53730a74`
- **Références sortantes (11) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CINEMATIC_INTEGRATION_GUIDE.md` *(l.13)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CINEMATIC_MODE_SUMMARY.md` *(l.14)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CINEMATIC_EXAMPLES.py` *(l.15)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CINEMATIC_DEPLOYMENT.md` *(l.16)*
  - ❓ `ref_generique` → `/home/agent/app/src/ui/` *(l.26)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\ui\cinematic_display.py` *(l.31)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\ui\cinematic_orchestrator.py` *(l.32)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\ui\complexity_analyzer.py` *(l.33)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\ui\cli.py` *(l.147)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docker-compose.yml` *(l.171)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\core\pipeline.py` *(l.202)*

### `agent-multiloop-Gabriel-local\CINEMATIC_EXAMPLES.py`
- **Type :** python
- **Taille :** 12.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 349
- **Hash MD5 :** `1994c5cb5d6d`
- **Références sortantes (7) :**
  - ❓ `import_module` → `asyncio` *(l.9)*
  - ❓ `import_module` → `logging` *(l.11)*
  - ❓ `import_module` → `typing` *(l.12)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\src\ui\complexity_analyzer.py` *(l.18)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\src\ui\cinematic_display.py` *(l.19)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\src\ui\cinematic_orchestrator.py` *(l.20)*
  - ❓ `import_module` → `time` *(l.306)*

### `agent-multiloop-Gabriel-local\CINEMATIC_INTEGRATION_GUIDE.md`
- **Type :** markdown
- **Taille :** 13.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 353
- **Hash MD5 :** `0db6999ebf95`
- **Références sortantes (3) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.26)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\ui\complexity_analyzer.py` *(l.164)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\ui\ask_gabriel.py` *(l.219)*

### `agent-multiloop-Gabriel-local\CINEMATIC_MODE_SUMMARY.md`
- **Type :** markdown
- **Taille :** 9.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 303
- **Hash MD5 :** `f0ff7be40c6a`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\ui\complexity_analyzer.py` *(l.178)*

### `agent-multiloop-Gabriel-local\CLAUDE_BUDGET_GUIDE.md`
- **Type :** markdown
- **Taille :** 6.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 289
- **Hash MD5 :** `976486e58b81`
- **Références sortantes (3) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\llm_router.py` *(l.39)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\cost_manager.py` *(l.49)*
  - ❓ `ref_generique` → `//console.anthropic.com/usage` *(l.204)*

### `agent-multiloop-Gabriel-local\COMMANDES_PRATIQUES_ANALYSE.md`
- **Type :** markdown
- **Taille :** 5.9 Ko
- **Modifié :** 2026-08-15 07:57:00
- **Lignes :** 212
- **Hash MD5 :** `a3163aaafb92`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.168)*

### `agent-multiloop-Gabriel-local\COMMANDS_COMPLETE_REFERENCE.md`
- **Type :** markdown
- **Taille :** 14.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 582
- **Hash MD5 :** `1fb0f4f69002`
- **Références sortantes (12) :**
  - ❓ `ref_generique` → `//localhost` *(l.87)*
  - ❓ `ref_generique` → `/theories/projects/` *(l.151)*
  - ❓ `ref_generique` → `/theories/projects/txt/` *(l.157)*
  - ❓ `ref_generique` → `/theories/projects/tex/` *(l.163)*
  - ❓ `ref_generique` → `/theories/projects/projet_uni_car_savard_01.thy` *(l.179)*
  - ❓ `ref_generique` → `/theories` *(l.189)*
  - ❓ `ref_generique` → `/theories/projects/exemple.thy` *(l.242)*
  - ❓ `ref_generique` → `/theories/projects/projet_uni_car_savard_26.thy` *(l.325)*
  - ❓ `ref_generique` → `/theories/projects/tex` *(l.335)*
  - ❓ `ref_generique` → `/theories/projects/projet_uni_car_savard_` *(l.346)*
  - ❓ `ref_generique` → `/home/agent/app/data` *(l.461)*
  - ❓ `ref_generique` → `/home/agent/app/` *(l.466)*

### `agent-multiloop-Gabriel-local\COMPLETE_INTEGRATION_INSTRUCTIONS.md`
- **Type :** markdown
- **Taille :** 16.7 Ko
- **Modifié :** 2026-08-16 20:13:50
- **Lignes :** 410
- **Hash MD5 :** `cc055b47d9b5`
- **Références sortantes (2) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\ui\cli.py` *(l.273)*
  - ❓ `ref_generique` → `./test.png` *(l.399)*

### `agent-multiloop-Gabriel-local\CONFIG_ENV_GUIDE.md`
- **Type :** markdown
- **Taille :** 6.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 157
- **Hash MD5 :** `12107a810b06`
- **Références sortantes (4) :**
  - ❓ `ref_generique` → `/home/agent/app/.env` *(l.12)*
  - ❓ `ref_generique` → `./.env:/home/agent/app/.env:ro`.` *(l.19)*
  - ❓ `ref_generique` → `Emergent.sh` *(l.120)*
  - ❓ `ref_generique` → `//console.anthropic.com/settings/keys` *(l.141)*

### `agent-multiloop-Gabriel-local\COPIER_COLLER_DIRECT.py`
- **Type :** python
- **Taille :** 3.8 Ko
- **Modifié :** 2026-08-15 07:42:11
- **Lignes :** 119
- **Hash MD5 :** `96313c5514ae`
- **Références sortantes (1) :**
  - ❓ `import_module` → `src.gabriel_image_interface` *(l.52)*

### `agent-multiloop-Gabriel-local\CORRECTION_ERREUR_TCHEBYCHEV_GABRIEL.md`
- **Type :** markdown
- **Taille :** 4.7 Ko
- **Modifié :** 2026-08-15 19:34:33
- **Lignes :** 192
- **Hash MD5 :** `bf46535600f8`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\CORRECTION_RSA_v2.2.md`
- **Type :** markdown
- **Taille :** 6.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 280
- **Hash MD5 :** `bec00b5894e4`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\test_rsa_capability.py` *(l.129)*

### `agent-multiloop-Gabriel-local\DEPLOYMENT_CHECKLIST_v4.0.md`
- **Type :** markdown
- **Taille :** 7.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 282
- **Hash MD5 :** `f06f0898f092`
- **Références sortantes (23) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docker-compose.yml` *(l.6)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\requirements.txt` *(l.7)*
  - ❓ `ref_generique` → `/query` *(l.39)*
  - ❓ `ref_generique` → `/sync/universestaucarre` *(l.44)*
  - ❓ `ref_generique` → `/isabelle/verify` *(l.49)*
  - ❓ `ref_generique` → `/data/isabelle-results/` *(l.51)*
  - ❓ `ref_generique` → `/health` *(l.54)*
  - ❓ `ref_generique` → `/stream` *(l.58)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\adapters\gabriel_isabelle_bridge.py` *(l.65)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.73)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\scripts\isabelle-integration.sh` *(l.81)*
  - ❓ `ref_generique` → `/theories` *(l.82)*
  - ❓ `ref_generique` → `/output/` *(l.86)*
  - ❓ `ref_generique` → `/tmp/.X11-unix` *(l.95)*
  - ❓ `ref_generique` → `README_v4.0.md` *(l.105)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\INTEGRATION_UNIVERSESTAUCARRE.md` *(l.106)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GUIDE_JEDIT_GABRIEL.md` *(l.107)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\JEDIT_QUICK_REFERENCE.md` *(l.108)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\quick-start.sh` *(l.109)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\test-integration.sh` *(l.110)*
  - ❓ `ref_generique` → `//localhost` *(l.125)*
  - ❓ `ref_generique` → `/data/universestaucarre-sync/` *(l.171)*
  - ❓ `ref_generique` → `/theories/generated/` *(l.199)*

### `agent-multiloop-Gabriel-local\DEPLOYMENT_READY.txt`
- **Type :** texte
- **Taille :** 11.1 Ko
- **Modifié :** 2026-08-16 20:17:47
- **Lignes :** 279
- **Hash MD5 :** `7cb75188b063`
- **Références sortantes (6) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\COMPLETE_INTEGRATION_INSTRUCTIONS.md` *(l.24)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\apply_image_analysis_patch.py` *(l.28)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\deploy_image_analysis.py` *(l.32)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\00_START_HERE_IMAGE_ANALYSIS.md` *(l.38)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\INTEGRATION_PATCH_IMAGE_ANALYSIS.md` *(l.39)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\ui\cli.py` *(l.216)*

### `agent-multiloop-Gabriel-local\DEPLOYMENT_SUMMARY.md`
- **Type :** markdown
- **Taille :** 8.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 307
- **Hash MD5 :** `272a1d3a3db1`
- **Références sortantes (10) :**
  - ❓ `ref_generique` → `config_mathematical.env` *(l.54)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\requirements.txt` *(l.65)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\gabriel_mathematical.py` *(l.78)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\quick_verification.py` *(l.232)*
  - ❓ `ref_generique` → `//docs.sympy.org/` *(l.265)*
  - ❓ `ref_generique` → `//mpmath.org/` *(l.266)*
  - ❓ `ref_generique` → `//github.com/HOL-Theorem-Prover/HOL` *(l.267)*
  - ❓ `ref_generique` → `//lean-lang.org/` *(l.268)*
  - ❓ `ref_generique` → `//pari.math.u-bordeaux.fr/` *(l.269)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` *(l.299)*

### `agent-multiloop-Gabriel-local\Dockerfile.cli`
- **Type :** autre
- **Taille :** 2.0 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 55
- **Hash MD5 :** `62b36c0059ab`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\ETAPE5_AMELIORATIONS_PRIORITAIRES.md`
- **Type :** markdown
- **Taille :** 7.1 Ko
- **Modifié :** 2026-08-15 08:48:14
- **Lignes :** 290
- **Hash MD5 :** `ded857c7321a`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\EXEMPLE_GABRIEL_v2.1.py`
- **Type :** python
- **Taille :** 9.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 278
- **Hash MD5 :** `5d82a9b7b6b6`
- **Références sortantes (1) :**
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\gabriel_mathematical.py` *(l.5)*

### `agent-multiloop-Gabriel-local\FILES_v5.0.md`
- **Type :** markdown
- **Taille :** 4.1 Ko
- **Modifié :** 2026-08-15 00:30:14
- **Lignes :** 190
- **Hash MD5 :** `caf51cce5625`
- **Références sortantes (1) :**
  - ❓ `ref_generique` → `//localhost` *(l.48)*

### `agent-multiloop-Gabriel-local\FINAL_300_TEMPLATES_SUMMARY.md`
- **Type :** markdown
- **Taille :** 8.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 305
- **Hash MD5 :** `313d48ab645e`
- **Références sortantes (16) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_01.thy` *(l.8)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_02.thy` *(l.9)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_100.thy` *(l.11)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_01.txt` *(l.20)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_02.txt` *(l.21)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_100.txt` *(l.23)*
  - ❓ `ref_generique` → `/theories/projects/` *(l.59)*
  - ❓ `ref_generique` → `/theories/projects/txt/` *(l.60)*
  - ❓ `ref_generique` → `/theories/projects/tex/` *(l.61)*
  - ❓ `ref_generique` → `/theories/projects` *(l.64)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_42.thy` *(l.83)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_42.txt` *(l.86)*
  - ❓ `ref_generique` → `//localhost` *(l.230)*
  - ❓ `ref_generique` → `/theories/projects/projet_uni_car_savard_01.thy` *(l.233)*
  - ❓ `ref_generique` → `/theories/projects/txt/projet_uni_car_savard_01.txt` *(l.234)*
  - ❓ `ref_generique` → `/theories/projects/tex/projet_uni_car_savard_01.tex` *(l.235)*

### `agent-multiloop-Gabriel-local\FINAL_RECONSTRUCTION_SUMMARY.txt`
- **Type :** texte
- **Taille :** 10.5 Ko
- **Modifié :** 2026-08-15 08:09:22
- **Lignes :** 225
- **Hash MD5 :** `dd026c819e3b`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\GABRIEL_COMPLETE_VISION_INTEGRATION.md`
- **Type :** markdown
- **Taille :** 7.8 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 277
- **Hash MD5 :** `90af01ad6e7e`
- **Références sortantes (15) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.4)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\ui\ask_gabriel.py` *(l.4)*
  - ❓ `ref_generique` → `result.py` *(l.32)*
  - ❓ `ref_generique` → `//github.com/UB-Mannheim/tesseract/wiki` *(l.113)*
  - ❓ `ref_generique` → `pytesseract.pytesseract.py` *(l.117)*
  - ❓ `ref_generique` → `/Gabriel/image_cache` *(l.128)*
  - ❓ `ref_generique` → `/Users/Philippe/Desktop/triangle.png` *(l.137)*
  - ❓ `ref_generique` → `//example.com/data_table.png` *(l.149)*
  - ❓ `ref_generique` → `analysis.json` *(l.188)*
  - ❓ `ref_generique` → `result.json` *(l.189)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\image_access_manager.py` *(l.196)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\vision_module.py` *(l.197)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\advanced_vision_module.py` *(l.198)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\gabriel_vision_integration.py` *(l.199)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\complete_vision_system.py` *(l.200)*

### `agent-multiloop-Gabriel-local\GABRIEL_DEBUGGER_PAUSE_STATUS.md`
- **Type :** markdown
- **Taille :** 2.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 55
- **Hash MD5 :** `002cd596b81f`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.15)*

### `agent-multiloop-Gabriel-local\GABRIEL_DOMAIN_SYSTEM_INTEGRATION_GUIDE.md`
- **Type :** markdown
- **Taille :** 10.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 355
- **Hash MD5 :** `68ba20b79611`
- **Références sortantes (2) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\multiloop\slow_motion_debugger.py` *(l.176)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\multiloop\domain_gate.py` *(l.316)*

### `agent-multiloop-Gabriel-local\GABRIEL_FINAL_SOLUTION.txt`
- **Type :** texte
- **Taille :** 5.9 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 275
- **Hash MD5 :** `89c78b99f988`
- **Références sortantes (1) :**
  - ❓ `ref_generique` → `//localhost` *(l.46)*

### `agent-multiloop-Gabriel-local\GABRIEL_FINAL_v5_SOCKET_CLEANUP.md`
- **Type :** markdown
- **Taille :** 5.5 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 204
- **Hash MD5 :** `d3732b33d1a6`
- **Références sortantes (4) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\socket_cleanup.py` *(l.75)*
  - ❓ `ref_generique` → `/home/agent/app/` *(l.75)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.76)*
  - ❓ `ref_generique` → `//localhost` *(l.89)*

### `agent-multiloop-Gabriel-local\GABRIEL_IMAGE_ANALYSIS_COMPLETE_GUIDE.md`
- **Type :** markdown
- **Taille :** 9.8 Ko
- **Modifié :** 2026-08-15 07:40:29
- **Lignes :** 396
- **Hash MD5 :** `b38aee7a0834`
- **Références sortantes (11) :**
  - ❓ `ref_generique` → `//localhost` *(l.80)*
  - ❓ `ref_generique` → `result.json` *(l.140)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.185)*
  - ❓ `ref_generique` → `./data/cache/vision` *(l.345)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\complete_vision_system.py` *(l.357)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\production_validation_system.py` *(l.358)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\image_access_manager.py` *(l.359)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\vision_module.py` *(l.360)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\advanced_vision_module.py` *(l.361)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\gabriel_image_interface.py` *(l.362)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\ui\cli.py` *(l.364)*

### `agent-multiloop-Gabriel-local\GABRIEL_PARAMETRIC_VALIDATION_GUIDE.md`
- **Type :** markdown
- **Taille :** 9.9 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 363
- **Hash MD5 :** `3d192c87e999`
- **Références sortantes (7) :**
  - ❓ `ref_generique` → `/schema/beau_soleil.png` *(l.97)*
  - ❓ `ref_generique` → `/figures/mon_triangle.png` *(l.115)*
  - ❓ `ref_generique` → `/cercle.png` *(l.137)*
  - ❓ `ref_generique` → `/triangle.png` *(l.154)*
  - ❓ `ref_generique` → `/rectangle.png` *(l.173)*
  - ❓ `ref_generique` → `/path/image.png` *(l.251)*
  - ❓ `ref_generique` → `/schema/figure.png` *(l.338)*

### `agent-multiloop-Gabriel-local\GABRIEL_PERFORMANCE_OPTIMIZATION.md`
- **Type :** markdown
- **Taille :** 3.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 97
- **Hash MD5 :** `5e487d4e68ce`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.77)*

### `agent-multiloop-Gabriel-local\GABRIEL_PORT_FIX_v5.3.md`
- **Type :** markdown
- **Taille :** 5.7 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 227
- **Hash MD5 :** `923b3d32ff33`
- **Références sortantes (5) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\gabriel_control.py` *(l.50)*
  - ❓ `ref_generique` → `//localhost` *(l.82)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docker-compose.yml` *(l.195)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\gabriel_launcher.py` *(l.196)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.196)*

### `agent-multiloop-Gabriel-local\GABRIEL_PRODUCTION_VALIDATION_GUIDE.md`
- **Type :** markdown
- **Taille :** 9.2 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 331
- **Hash MD5 :** `e6358002a642`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\GABRIEL_VALIDATION_EXAMPLES.md`
- **Type :** markdown
- **Taille :** 8.5 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 395
- **Hash MD5 :** `daf24ab390c9`
- **Références sortantes (10) :**
  - ❓ `ref_generique` → `/schema/beau_soleil.png` *(l.15)*
  - ❓ `ref_generique` → `/figures/mon_triangle.png` *(l.45)*
  - ❓ `ref_generique` → `/cercle.png` *(l.66)*
  - ❓ `ref_generique` → `/triangle.png` *(l.108)*
  - ❓ `ref_generique` → `/figure.png` *(l.147)*
  - ❓ `ref_generique` → `/rectangle.png` *(l.176)*
  - ❓ `ref_generique` → `/etoile.png` *(l.221)*
  - ❓ `ref_generique` → `/soleil.png` *(l.257)*
  - ❓ `ref_generique` → `/schema/complexe.png` *(l.327)*
  - ❓ `ref_generique` → `/image.png` *(l.379)*

### `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md`
- **Type :** markdown
- **Taille :** 11.2 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 435
- **Hash MD5 :** `f1da4b1f484b`
- **Références sortantes (17) :**
  - ❓ `ref_generique` → `//serveur/partage/fichier.png` *(l.11)*
  - ❓ `ref_generique` → `//example.com/image.png` *(l.12)*
  - ❓ `ref_generique` → `/Users/Philippe/Pictures/geometrie.png` *(l.41)*
  - ❓ `ref_generique` → `./data/figures/triangle.jpg` *(l.42)*
  - ❓ `ref_generique` → `/home/user/images/schema.png` *(l.43)*
  - ❓ `ref_generique` → `result.py` *(l.47)*
  - ❓ `ref_generique` → `//example.com/my-figure.png` *(l.53)*
  - ❓ `ref_generique` → `//192.168.1.100/shared/diagram.png` *(l.67)*
  - ❓ `ref_generique` → `/path/to/triangle.png` *(l.81)*
  - ❓ `ref_generique` → `/tmp/gabriel_image_cache` *(l.157)*
  - ❓ `ref_generique` → `/MesDocuments/Figures` *(l.171)*
  - ❓ `ref_generique` → `/mnt/shared/diagrams` *(l.172)*
  - ❓ `ref_generique` → `/Users/Me/Desktop/triangle.png` *(l.223)*
  - ❓ `ref_generique` → `/Users/Philippe/Figures/schema.png` *(l.308)*
  - ❓ `ref_generique` → `triangle_param.py` *(l.356)*
  - ❓ `ref_generique` → `triangle_formal.thy` *(l.360)*
  - ❓ `ref_generique` → `result.sh` *(l.378)*

### `agent-multiloop-Gabriel-local\GABRIEL_VISION_QUICK_START.md`
- **Type :** markdown
- **Taille :** 5.2 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 189
- **Hash MD5 :** `c2b7c2a52b5b`
- **Références sortantes (19) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\image_access_manager.py` *(l.7)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\vision_module.py` *(l.8)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\advanced_vision_module.py` *(l.9)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\gabriel_vision_integration.py` *(l.10)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\complete_vision_system.py` *(l.11)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` *(l.14)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_COMPLETE_VISION_INTEGRATION.md` *(l.15)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_VISION_VERIFICATION_COMPLETE.md` *(l.16)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.40)*
  - ❓ `ref_generique` → `./test_image.png` *(l.51)*
  - ❓ `ref_generique` → `/path/to/figure.png` *(l.58)*
  - ❓ `ref_generique` → `//example.com/chart.png` *(l.59)*
  - ❓ `ref_generique` → `./data/spreadsheet_screenshot.png` *(l.61)*
  - ❓ `ref_generique` → `./image_cache` *(l.111)*
  - ❓ `ref_generique` → `/Users/Philippe/Desktop/mon_schema.png` *(l.115)*
  - ❓ `ref_generique` → `result.py` *(l.129)*
  - ❓ `ref_generique` → `analysis.json` *(l.136)*
  - ❓ `ref_generique` → `result.json` *(l.137)*
  - ❓ `ref_generique` → `//github.com/UB-Mannheim/tesseract/wiki` *(l.159)*

### `agent-multiloop-Gabriel-local\GABRIEL_VISION_VERIFICATION_COMPLETE.md`
- **Type :** markdown
- **Taille :** 7.4 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 249
- **Hash MD5 :** `3fe8e6bfafc6`
- **Références sortantes (9) :**
  - ❓ `ref_generique` → `//example.com/image.png` *(l.29)*
  - ❓ `ref_generique` → `//serveur/partage/fichier.png` *(l.31)*
  - ❓ `ref_generique` → `/path/to/image.png` *(l.171)*
  - ❓ `ref_generique` → `result.py` *(l.180)*
  - ❓ `ref_generique` → `result.json` *(l.183)*
  - ❓ `ref_generique` → `/Desktop/triangle.png` *(l.188)*
  - ❓ `ref_generique` → `//example.com/data.png` *(l.230)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.234)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_COMPLETE_VISION_INTEGRATION.md` *(l.234)*

### `agent-multiloop-Gabriel-local\GABRIEL_v2.1_RELEASE_NOTES.md`
- **Type :** markdown
- **Taille :** 6.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 244
- **Hash MD5 :** `8446388b2a4e`
- **Références sortantes (2) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\gabriel_mathematical.py` *(l.210)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\HOL4_SYSTEMATIC_PROOFS.md` *(l.212)*

### `agent-multiloop-Gabriel-local\GABRIEL_v2.2_RSA_CAPABILITY.md`
- **Type :** markdown
- **Taille :** 8.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 352
- **Hash MD5 :** `92a26db26b06`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\GABRIEL_v3.0_MULTILOOP_VALIDATION.md`
- **Type :** markdown
- **Taille :** 9.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 400
- **Hash MD5 :** `ef593d49f1d9`
- **Références sortantes (3) :**
  - ❓ `ref_generique` → `théorie.thy` *(l.33)*
  - ❓ `ref_generique` → `results.json` *(l.164)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\gabriel_mathematical.py` *(l.339)*

### `agent-multiloop-Gabriel-local\GABRIEL_v4.0_THEORY_MEMORY.md`
- **Type :** markdown
- **Taille :** 10.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 435
- **Hash MD5 :** `bc0eecabd9a7`
- **Références sortantes (5) :**
  - ✅ `ref_generique` → `memory\directives_theorie_savard.md` *(l.29)*
  - ✅ `ref_generique` → `memory\theory_axioms_manager.py` *(l.30)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\prompt_injector.py` *(l.31)*
  - ❓ `ref_generique` → `axioms.json` *(l.32)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\gabriel_mathematical.py` *(l.232)*

### `agent-multiloop-Gabriel-local\GABRIEL_v5.0_FINAL_SUMMARY.txt`
- **Type :** texte
- **Taille :** 4.9 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 245
- **Hash MD5 :** `104f8b54ff1f`
- **Références sortantes (5) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\socket_cleanup.py` *(l.66)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.87)*
  - ❓ `ref_generique` → `//localhost` *(l.127)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_FINAL_v5_SOCKET_CLEANUP.md` *(l.243)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v5_UPDATE_GUIDE.md` *(l.244)*

### `agent-multiloop-Gabriel-local\GABRIEL_v5.0_LLM_ROUTING.md`
- **Type :** markdown
- **Taille :** 9.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 395
- **Hash MD5 :** `69398b013a03`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\GABRIEL_v5.1_SAFE_BUDGET.md`
- **Type :** markdown
- **Taille :** 8.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 322
- **Hash MD5 :** `c1e3abf426e3`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\GABRIEL_v5.2_DEPLOYMENT_SUMMARY.md`
- **Type :** markdown
- **Taille :** 10.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 410
- **Hash MD5 :** `cc5406af6aa5`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\GABRIEL_v5.2_HOL_FORMAL.md`
- **Type :** markdown
- **Taille :** 9.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 360
- **Hash MD5 :** `af93d218abad`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\GABRIEL_v5.4_WORKING_SOLUTION.md`
- **Type :** markdown
- **Taille :** 3.5 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 131
- **Hash MD5 :** `35480b540c1b`
- **Références sortantes (3) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.26)*
  - ❓ `ref_generique` → `//localhost` *(l.60)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\gabriel_launcher.py` *(l.82)*

### `agent-multiloop-Gabriel-local\GABRIEL_v5_EXPLIQUE_SIMPLEMENT.txt`
- **Type :** texte
- **Taille :** 4.9 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 234
- **Hash MD5 :** `68a98dbabcfe`
- **Références sortantes (1) :**
  - ❓ `ref_generique` → `//localhost` *(l.124)*

### `agent-multiloop-Gabriel-local\GABRIEL_v5_UPDATE_GUIDE.md`
- **Type :** markdown
- **Taille :** 5.0 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 268
- **Hash MD5 :** `0f21d0d7ba66`
- **Références sortantes (1) :**
  - ❓ `ref_generique` → `//localhost` *(l.82)*

### `agent-multiloop-Gabriel-local\GO_QUICK_START.md`
- **Type :** markdown
- **Taille :** 953.0 o
- **Modifié :** 2026-08-15 08:09:44
- **Lignes :** 31
- **Hash MD5 :** `e883f0669da7`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\GUIDE_ANALYSE_AVEC_CRITERES.md`
- **Type :** markdown
- **Taille :** 13.6 Ko
- **Modifié :** 2026-08-15 07:53:55
- **Lignes :** 555
- **Hash MD5 :** `95f319207783`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.398)*

### `agent-multiloop-Gabriel-local\GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md`
- **Type :** markdown
- **Taille :** 15.3 Ko
- **Modifié :** 2026-08-15 07:51:40
- **Lignes :** 681
- **Hash MD5 :** `3a2c9445fece`
- **Références sortantes (7) :**
  - ❓ `ref_generique` → `spectral_matrix_n50.json` *(l.99)*
  - ❓ `ref_generique` → `spectral_matrix_n50.py` *(l.101)*
  - ❓ `ref_generique` → `./figures/quadrature.png` *(l.263)*
  - ❓ `ref_generique` → `./figures/diagram.png` *(l.365)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.401)*
  - ❓ `ref_generique` → `matplotlib.py` *(l.501)*
  - ❓ `ref_generique` → `plt.sh` *(l.520)*

### `agent-multiloop-Gabriel-local\GUIDE_JEDIT_GABRIEL.md`
- **Type :** markdown
- **Taille :** 11.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 354
- **Hash MD5 :** `a36bacad3123`
- **Références sortantes (16) :**
  - ❓ `ref_generique` → `theorem_proof.thy` *(l.10)*
  - ❓ `ref_generique` → `/theories/generated_` *(l.12)*
  - ❓ `ref_generique` → `//sourceforge.net/projects/vcxsrv/` *(l.42)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docker-compose.yml` *(l.45)*
  - ❓ `ref_generique` → `./theories:/theories` *(l.64)*
  - ❓ `ref_generique` → `/home/isabelle/.isabelle/heaps` *(l.65)*
  - ❓ `ref_generique` → `/tmp/.X11-unix` *(l.67)*
  - ❓ `ref_generique` → `/bin/bash` *(l.72)*
  - ❓ `ref_generique` → `/dev/null` *(l.73)*
  - ❓ `ref_generique` → `/theories/example.thy` *(l.89)*
  - ❓ `ref_generique` → `/theories/generated/` *(l.107)*
  - ❓ `ref_generique` → `/theories/generated_1234567890.thy` *(l.130)*
  - ❓ `ref_generique` → `/theories` *(l.238)*
  - ❓ `ref_generique` → `//localhost` *(l.273)*
  - ❓ `ref_generique` → `/query` *(l.291)*
  - ❓ `ref_generique` → `/theories/generated.thy` *(l.308)*

### `agent-multiloop-Gabriel-local\GUIDE_RECONSTRUCTION_REDEMARRAGE.md`
- **Type :** markdown
- **Taille :** 7.6 Ko
- **Modifié :** 2026-08-15 08:08:12
- **Lignes :** 343
- **Hash MD5 :** `5292ea9269a3`
- **Références sortantes (2) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.56)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\requirements.txt` *(l.182)*

### `agent-multiloop-Gabriel-local\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.aux`
- **Type :** autre
- **Taille :** 11.2 Ko
- **Modifié :** 2026-08-07 07:32:07
- **Lignes :** 173
- **Hash MD5 :** `c03c2ed58b35`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.listing`
- **Type :** autre
- **Taille :** 1.5 Ko
- **Modifié :** 2026-08-07 07:32:07
- **Lignes :** 39
- **Hash MD5 :** `ab594b247975`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.log`
- **Type :** autre
- **Taille :** 60.6 Ko
- **Modifié :** 2026-08-07 07:32:07
- **Lignes :** 1709
- **Hash MD5 :** `5d1c119030da`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.out`
- **Type :** autre
- **Taille :** 13.4 Ko
- **Modifié :** 2026-08-07 07:32:07
- **Lignes :** 46
- **Hash MD5 :** `a0d03ef2b623`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.toc`
- **Type :** autre
- **Taille :** 6.0 Ko
- **Modifié :** 2026-08-07 07:32:07
- **Lignes :** 56
- **Hash MD5 :** `e864678074b9`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\HOL4_SYSTEMATIC_PROOFS.md`
- **Type :** markdown
- **Taille :** 7.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 288
- **Hash MD5 :** `397c46f4d30b`
- **Références sortantes (2) :**
  - ❓ `ref_generique` → `riemann_spectral.thy` *(l.71)*
  - ❓ `ref_generique` → `result_proof.thy` *(l.193)*

### `agent-multiloop-Gabriel-local\HOL_ISABELLE_FIX.md`
- **Type :** markdown
- **Taille :** 4.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 193
- **Hash MD5 :** `f77b129cbf07`
- **Références sortantes (3) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\spectral\hol_script_generator.py` *(l.43)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\adapters\hol_integration.py` *(l.56)*
  - ❓ `ref_generique` → `/theories` *(l.151)*

### `agent-multiloop-Gabriel-local\IMAGE_ANALYSIS_ANSWER_DIRECT.md`
- **Type :** markdown
- **Taille :** 5.9 Ko
- **Modifié :** 2026-08-15 07:41:34
- **Lignes :** 257
- **Hash MD5 :** `48a623b394c0`
- **Références sortantes (1) :**
  - ❓ `ref_generique` → `//localhost` *(l.230)*

### `agent-multiloop-Gabriel-local\INDEX.md`
- **Type :** markdown
- **Taille :** 5.7 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 256
- **Hash MD5 :** `6a57d9b60862`
- **Références sortantes (8) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\gabriel_launcher.py` *(l.85)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\START_HERE.txt` *(l.136)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` *(l.138)*
  - ❓ `ref_generique` → `//localhost` *(l.146)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\QUICK_REFERENCE.md` *(l.207)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\POWERSHELL_ISE_GUIDE.md` *(l.208)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\SHORTCUTS_AND_TIPS.md` *(l.209)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docker-compose.yml` *(l.210)*

### `agent-multiloop-Gabriel-local\INTEGRATION_MANUELLE.py`
- **Type :** python
- **Taille :** 3.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 92
- **Hash MD5 :** `1e604f0be15c`
- **Références sortantes (1) :**
  - ❓ `import_module` → `.cinematic_orchestrator` *(l.24)*

### `agent-multiloop-Gabriel-local\INTEGRATION_PATCH_IMAGE_ANALYSIS.md`
- **Type :** markdown
- **Taille :** 6.9 Ko
- **Modifié :** 2026-08-16 20:07:32
- **Lignes :** 214
- **Hash MD5 :** `327e34d82dde`
- **Références sortantes (5) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\ui\cli.py` *(l.14)*
  - ❓ `ref_generique` → `/path/image.png` *(l.44)*
  - ❓ `ref_generique` → `/path/to/file.ext` *(l.124)*
  - ❓ `ref_generique` → `./path` *(l.130)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\gabriel_vision_integration.py` *(l.161)*

### `agent-multiloop-Gabriel-local\INTEGRATION_UNIVERSESTAUCARRE.md`
- **Type :** markdown
- **Taille :** 10.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 361
- **Hash MD5 :** `e0c35753e0c8`
- **Références sortantes (13) :**
  - ❓ `ref_generique` → `emergent.sh` *(l.8)*
  - ❓ `ref_generique` → `/sync/universestaucarre` *(l.11)*
  - ❓ `ref_generique` → `/query` *(l.18)*
  - ❓ `ref_generique` → `/isabelle/verify` *(l.20)*
  - ❓ `ref_generique` → `/health` *(l.21)*
  - ❓ `ref_generique` → `//localhost` *(l.50)*
  - ❓ `ref_generique` → `//0.0.0.0` *(l.53)*
  - ❓ `ref_generique` → `response.json` *(l.87)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docker-compose.yml` *(l.114)*
  - ❓ `ref_generique` → `//192.168.1.100` *(l.123)*
  - ❓ `ref_generique` → `//gabriel-local.home` *(l.125)*
  - ❓ `ref_generique` → `/home/agent/app/data/universestaucarre-sync/` *(l.245)*
  - ❓ `ref_generique` → `//gabriel` *(l.293)*

### `agent-multiloop-Gabriel-local\JEDIT_QUICK_REFERENCE.md`
- **Type :** markdown
- **Taille :** 6.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 285
- **Hash MD5 :** `8195f6d9d102`
- **Références sortantes (10) :**
  - ❓ `ref_generique` → `/theories/example.thy` *(l.15)*
  - ❓ `ref_generique` → `/theories/file.thy` *(l.26)*
  - ❓ `ref_generique` → `//localhost` *(l.65)*
  - ❓ `ref_generique` → `/theories/generated_1234567890.thy` *(l.87)*
  - ❓ `ref_generique` → `generated_1234567890.thy` *(l.94)*
  - ❓ `ref_generique` → `//sourceforge.net/projects/vcxsrv/` *(l.157)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.187)*
  - ❓ `ref_generique` → `/theories/generated/` *(l.218)*
  - ❓ `ref_generique` → `//0.0.0.0` *(l.225)*
  - ❓ `ref_generique` → `/theories` *(l.263)*

### `agent-multiloop-Gabriel-local\MIGRATION_VALIDATION_SYSTEMS.md`
- **Type :** markdown
- **Taille :** 6.7 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 290
- **Hash MD5 :** `34c4ed4efe3d`
- **Références sortantes (5) :**
  - ❓ `ref_generique` → `/schema/beau_soleil.png` *(l.9)*
  - ❓ `ref_generique` → `/schema/soleil.png` *(l.66)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\parametric_validation_module.py` *(l.266)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\complete_validation_integration.py` *(l.267)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\production_validation_system.py` *(l.270)*

### `agent-multiloop-Gabriel-local\MOT_FIN_SESSION.txt`
- **Type :** texte
- **Taille :** 13.0 Ko
- **Modifié :** 2026-08-15 08:20:35
- **Lignes :** 279
- **Hash MD5 :** `f916a49cbda7`
- **Références sortantes (14) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\gabriel_image_interface.py` *(l.42)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\image_discovery_system.py` *(l.43)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\advanced_analysis_criteria.py` *(l.44)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\validation_hol_knowledge.py` *(l.54)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GO_QUICK_START.md` *(l.152)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\QUICK_START_5_MINUTES.md` *(l.153)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\REPONSE_RAPIDE_RECONSTRUCTION.md` *(l.154)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md` *(l.157)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_IMAGE_ANALYSIS_COMPLETE_GUIDE.md` *(l.158)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GUIDE_ANALYSE_AVEC_CRITERES.md` *(l.159)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\COMMANDES_PRATIQUES_ANALYSE.md` *(l.160)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\RAPPORT_ANALYSE_DEPENDANCES.md` *(l.163)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\VERIFICATION_FINALE_SYNTHESE.txt` *(l.164)*
  - ✅ `ref_generique` → `PLAN_ORGANISATION.md` *(l.165)*

### `agent-multiloop-Gabriel-local\MULTIFORMAT_TEMPLATES_GUIDE.md`
- **Type :** markdown
- **Taille :** 10.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 417
- **Hash MD5 :** `be89b61b177c`
- **Références sortantes (21) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_01.thy` *(l.9)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_02.thy` *(l.10)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_100.thy` *(l.12)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_01.txt` *(l.15)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_02.txt` *(l.16)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_100.txt` *(l.18)*
  - ❓ `ref_generique` → `/theories/projects/projet_uni_car_savard_26.thy` *(l.169)*
  - ❓ `ref_generique` → `/theories/projects/txt/projet_uni_car_savard_26.txt` *(l.174)*
  - ❓ `ref_generique` → `/theories/projects/tex/projet_uni_car_savard_26.tex` *(l.178)*
  - ❓ `ref_generique` → `/theories/projects/` *(l.199)*
  - ❓ `ref_generique` → `/theories/projects/txt/` *(l.200)*
  - ❓ `ref_generique` → `/theories/projects/tex/` *(l.201)*
  - ❓ `ref_generique` → `/theories/projects/txt/projet_uni_car_savard_42.txt` *(l.204)*
  - ❓ `ref_generique` → `/theories/projects` *(l.220)*
  - ❓ `ref_generique` → `self.thy` *(l.222)*
  - ❓ `ref_generique` → `self.txt` *(l.223)*
  - ❓ `ref_generique` → `./theories:/theories` *(l.284)*
  - ❓ `ref_generique` → `/theories/projects/projet_uni_car_savard_42.thy` *(l.304)*
  - ❓ `ref_generique` → `/theories/projects/tex/projet_uni_car_savard_42.tex` *(l.306)*
  - ❓ `ref_generique` → `/theories/projects/tex` *(l.309)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_42.thy` *(l.340)*

### `agent-multiloop-Gabriel-local\OPTIMIZATION_SUMMARY.md`
- **Type :** markdown
- **Taille :** 6.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 145
- **Hash MD5 :** `e5c5f74b32bd`
- **Références sortantes (2) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\config_optimized.yaml` *(l.66)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\apply_optimization.py` *(l.67)*

### `agent-multiloop-Gabriel-local\ORGANISATION_GUIDE_UTILISATEUR_COMPLETE.txt`
- **Type :** texte
- **Taille :** 11.6 Ko
- **Modifié :** 2026-08-15 12:49:35
- **Lignes :** 279
- **Hash MD5 :** `52af8af3e057`
- **Références sortantes (55) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README.md` *(l.22)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\INDEX.md` *(l.24)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\QUICK_START_5_MINUTES.md` *(l.85)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GO_QUICK_START.md` *(l.86)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\QUICK_REFERENCE.md` *(l.87)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md` *(l.91)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CINEMATIC_MODE_SUMMARY.md` *(l.92)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CINEMATIC_INTEGRATION_GUIDE.md` *(l.93)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CINEMATIC_EXAMPLES.py` *(l.94)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CINEMATIC_DEPLOYMENT.md` *(l.95)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md` *(l.99)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GUIDE_ANALYSE_AVEC_CRITERES.md` *(l.100)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_IMAGE_ANALYSIS_COMPLETE_GUIDE.md` *(l.101)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_VISION_QUICK_START.md` *(l.102)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_VISION_VERIFICATION_COMPLETE.md` *(l.103)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` *(l.104)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\QUICK_START_IMAGE_ANALYSIS.md` *(l.105)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` *(l.109)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\DEPLOYMENT_SUMMARY.md` *(l.110)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\DEPLOYMENT_CHECKLIST_v4.0.md` *(l.111)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_PORT_FIX_v5.3.md` *(l.112)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PORT_CLEANUP_IMPLEMENTATION.md` *(l.113)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` *(l.117)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v4.0_THEORY_MEMORY.md` *(l.118)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v5.0_LLM_ROUTING.md` *(l.119)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_PARAMETRIC_VALIDATION_GUIDE.md` *(l.120)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\HOL_ISABELLE_FIX.md` *(l.121)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\HOL4_SYSTEMATIC_PROOFS.md` *(l.122)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v5.2_HOL_FORMAL.md` *(l.123)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GUIDE_RECONSTRUCTION_REDEMARRAGE.md` *(l.127)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\REPONSE_RAPIDE_RECONSTRUCTION.md` *(l.128)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_COMPLETE_VISION_INTEGRATION.md` *(l.129)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PYTEST_SUMMARY.md` *(l.133)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PYTEST_EXECUTION_GUIDE.md` *(l.134)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PYTEST_CHECKLIST.md` *(l.135)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PYTEST_LIST_COMPLETE.md` *(l.136)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PYTEST_INDEX.md` *(l.137)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_PRODUCTION_VALIDATION_GUIDE.md` *(l.138)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_VALIDATION_EXAMPLES.md` *(l.139)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CONFIG_ENV_GUIDE.md` *(l.143)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CLAUDE_BUDGET_GUIDE.md` *(l.144)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\POWERSHELL_ISE_GUIDE.md` *(l.145)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\JEDIT_QUICK_REFERENCE.md` *(l.146)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GUIDE_JEDIT_GABRIEL.md` *(l.147)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\COMMANDS_COMPLETE_REFERENCE.md` *(l.152)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\COMMANDES_PRATIQUES_ANALYSE.md` *(l.153)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\SHORTCUTS_AND_TIPS.md` *(l.154)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\RAPPORT_ETAPE1_ANALYSE_README.md` *(l.159)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\RAPPORT_ETAPE2_ANALYSE_ARCHITECTURE.md` *(l.160)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\RAPPORT_MAINTENANCE_ETAPE3.md` *(l.161)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\RAPPORT_ANALYSE_DEPENDANCES.md` *(l.162)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\RELEASE_NOTES_v2.1.md` *(l.166)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\ETAPE5_AMELIORATIONS_PRIORITAIRES.md` *(l.167)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\RELEASE_v2.1_COMPLETE.txt` *(l.168)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CHANGELOG.md` *(l.169)*

### `agent-multiloop-Gabriel-local\PATCH_IMAGE_ANALYSIS_INTEGRATION.py`
- **Type :** python
- **Taille :** 4.8 Ko
- **Modifié :** 2026-08-15 07:40:42
- **Lignes :** 133
- **Hash MD5 :** `36f551cce2d8`
- **Références sortantes (3) :**
  - ❓ `import_module` → `src.gabriel_image_interface` *(l.46)*
  - ❓ `chemin_litteral` → `/api/v1/image/analyze` *(l.87)*
  - ❓ `chemin_litteral` → `1. Ouvrir src/ui/cli.py` *(l.126)*

### `agent-multiloop-Gabriel-local\PATCH_THEORETICAL_RECOGNITION.md`
- **Type :** markdown
- **Taille :** 2.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 73
- **Hash MD5 :** `5723997ff3da`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\PORT_CLEANUP_IMPLEMENTATION.md`
- **Type :** markdown
- **Taille :** 8.2 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 270
- **Hash MD5 :** `b9e44376093f`
- **Références sortantes (10) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\gabriel_launcher.py` *(l.40)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.40)*
  - ❓ `ref_generique` → `./gabriel_launcher.py:/home/agent/app/gabriel_launcher.py` *(l.43)*
  - ❓ `ref_generique` → `./port_cleanup.py:/home/agent/app/port_cleanup.py` *(l.44)*
  - ❓ `ref_generique` → `./theories:/home/agent/app/theories` *(l.82)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\tex` *(l.82)*
  - ❓ `ref_generique` → `/home/agent/app/theories/tex/` *(l.87)*
  - ❓ `ref_generique` → `/home/agent/app/theories/tex/Geometrie_du_Spectre_des_Nombres_Premiers_2026.pdf` *(l.98)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\tex\README_pdf.md` *(l.118)*
  - ❓ `ref_generique` → `/theories/tex/` *(l.269)*

### `agent-multiloop-Gabriel-local\POWERSHELL_ISE_GUIDE.md`
- **Type :** markdown
- **Taille :** 5.1 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 232
- **Hash MD5 :** `8c0f606a0ad3`
- **Références sortantes (1) :**
  - ❓ `ref_generique` → `//localhost` *(l.29)*

### `agent-multiloop-Gabriel-local\PROJECTS_TEMPLATES_GUIDE.md`
- **Type :** markdown
- **Taille :** 8.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 313
- **Hash MD5 :** `b7a2bfa13645`
- **Références sortantes (18) :**
  - ❓ `ref_generique` → `/theories/projects/projet_uni_car_savard_` *(l.29)*
  - ❓ `ref_generique` → `/generated/` *(l.41)*
  - ❓ `ref_generique` → `/theories/generated/projet_uni_car_savard_` *(l.42)*
  - ❓ `ref_generique` → `/theories/projects/` *(l.104)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_01.thy` *(l.105)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_02.thy` *(l.106)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_100.thy` *(l.108)*
  - ❓ `ref_generique` → `/theories/projects/projet_uni_car_savard_42.thy` *(l.111)*
  - ❓ `ref_generique` → `/theories/projects/projet_uni_car_savard_15.thy` *(l.139)*
  - ❓ `ref_generique` → `/theories/archives/completed_15.thy` *(l.163)*
  - ❓ `ref_generique` → `/theories/projects` *(l.181)*
  - ❓ `ref_generique` → `/theories/generated/` *(l.232)*
  - ❓ `ref_generique` → `execution_projet_01.thy` *(l.248)*
  - ❓ `ref_generique` → `execution_projet_02.thy` *(l.249)*
  - ❓ `ref_generique` → `completed_01.thy` *(l.253)*
  - ❓ `ref_generique` → `./theories:/theories` *(l.266)*
  - ❓ `ref_generique` → `./theories:/home/agent/app/theories:ro` *(l.267)*
  - ❓ `ref_generique` → `/theories/projects/projet_uni_car_savard_01.thy` *(l.303)*

### `agent-multiloop-Gabriel-local\PYTEST_CHECKLIST.md`
- **Type :** markdown
- **Taille :** 6.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 213
- **Hash MD5 :** `fe722b55dfba`
- **Références sortantes (4) :**
  - ❓ `ref_generique` → `/home/agent/app` *(l.29)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\spectral\prime_table.py` *(l.130)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\spectral\gap_solver_corrected.py` *(l.131)*
  - ❓ `ref_generique` → `rapport_tests.txt` *(l.149)*

### `agent-multiloop-Gabriel-local\PYTEST_EXECUTION_GUIDE.md`
- **Type :** markdown
- **Taille :** 6.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 187
- **Hash MD5 :** `0652c8354b59`
- **Références sortantes (1) :**
  - ❓ `ref_generique` → `/home/agent/app` *(l.53)*

### `agent-multiloop-Gabriel-local\PYTEST_INDEX.md`
- **Type :** markdown
- **Taille :** 5.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 198
- **Hash MD5 :** `c8ed094663de`
- **Références sortantes (1) :**
  - ❓ `ref_generique` → `/home/agent/app` *(l.88)*

### `agent-multiloop-Gabriel-local\PYTEST_LIST_COMPLETE.md`
- **Type :** markdown
- **Taille :** 5.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 198
- **Hash MD5 :** `93f436895ba8`
- **Références sortantes (1) :**
  - ❓ `ref_generique` → `/home/agent/app` *(l.156)*

### `agent-multiloop-Gabriel-local\PYTEST_SUMMARY.md`
- **Type :** markdown
- **Taille :** 5.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 171
- **Hash MD5 :** `e670399b2473`
- **Références sortantes (1) :**
  - ❓ `ref_generique` → `/home/agent/app` *(l.156)*

### `agent-multiloop-Gabriel-local\QUICK_REFERENCE.md`
- **Type :** markdown
- **Taille :** 3.4 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 163
- **Hash MD5 :** `3132ebdd959a`
- **Références sortantes (3) :**
  - ❓ `ref_generique` → `//localhost` *(l.52)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docker-compose.yml` *(l.151)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_FINAL_SOLUTION.txt` *(l.152)*

### `agent-multiloop-Gabriel-local\QUICK_START_5_MINUTES.md`
- **Type :** markdown
- **Taille :** 4.1 Ko
- **Modifié :** 2026-08-15 07:43:11
- **Lignes :** 180
- **Hash MD5 :** `4e6172d114fe`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.66)*

### `agent-multiloop-Gabriel-local\QUICK_START_IMAGE_ANALYSIS.md`
- **Type :** markdown
- **Taille :** 8.2 Ko
- **Modifié :** 2026-08-15 07:41:06
- **Lignes :** 354
- **Hash MD5 :** `31c1676a98b0`
- **Références sortantes (3) :**
  - ❓ `ref_generique` → `//localhost` *(l.16)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\validation_hol_unifiee.thy` *(l.273)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_IMAGE_ANALYSIS_COMPLETE_GUIDE.md` *(l.334)*

### `agent-multiloop-Gabriel-local\RAPPORT_ANALYSE_DEPENDANCES.md`
- **Type :** markdown
- **Taille :** 5.9 Ko
- **Modifié :** 2026-08-15 08:18:34
- **Lignes :** 267
- **Hash MD5 :** `03a4d5d3c245`
- **Références sortantes (51) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\FINAL_RECONSTRUCTION_SUMMARY.txt` *(l.50)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GUIDE_RECONSTRUCTION_REDEMARRAGE.md` *(l.51)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\REPONSE_RAPIDE_RECONSTRUCTION.md` *(l.52)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GO_QUICK_START.md` *(l.53)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GUIDE_ANALYSE_AVEC_CRITERES.md` *(l.54)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\COMMANDES_PRATIQUES_ANALYSE.md` *(l.55)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md` *(l.56)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\IMAGE_ANALYSIS_ANSWER_DIRECT.md` *(l.57)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\QUICK_START_IMAGE_ANALYSIS.md` *(l.58)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\QUICK_START_5_MINUTES.md` *(l.59)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_IMAGE_ANALYSIS_COMPLETE_GUIDE.md` *(l.60)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_VISION_QUICK_START.md` *(l.61)*
  - ✅ `ref_generique` → `PLAN_ORGANISATION.md` *(l.81)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` *(l.104)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_VISION_VERIFICATION_COMPLETE.md` *(l.105)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_COMPLETE_VISION_INTEGRATION.md` *(l.106)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\VALIDATION_HOL_UNIFIEE_ANALYSIS.md` *(l.112)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\VALIDATION_HOL_INTEGRATION_COMPLETE.md` *(l.113)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CONFIG_ENV_GUIDE.md` *(l.119)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` *(l.120)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\UTF8_ENCODING_FIX.md` *(l.121)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PYTEST_CHECKLIST.md` *(l.127)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PYTEST_EXECUTION_GUIDE.md` *(l.128)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PYTEST_INDEX.md` *(l.129)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PYTEST_LIST_COMPLETE.md` *(l.130)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PYTEST_SUMMARY.md` *(l.131)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v2.1_RELEASE_NOTES.md` *(l.137)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v2.2_RSA_CAPABILITY.md` *(l.138)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v3.0_MULTILOOP_VALIDATION.md` *(l.139)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v4.0_THEORY_MEMORY.md` *(l.140)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v5.0_LLM_ROUTING.md` *(l.141)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v5.1_SAFE_BUDGET.md` *(l.142)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v5.2_DEPLOYMENT_SUMMARY.md` *(l.143)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v5.2_HOL_FORMAL.md` *(l.144)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v5_UPDATE_GUIDE.md` *(l.145)*
  - ❓ `ref_generique` → `README_FINAL.md` *(l.146)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` *(l.147)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md` *(l.148)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CHANGELOG.md` *(l.154)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CHECKLIST_FINAL.md` *(l.155)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\TODO_ANALYSE.md` *(l.156)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\FILES_v5.0.md` *(l.157)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\FINAL_300_TEMPLATES_SUMMARY.md` *(l.158)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CLAUDE_BUDGET_GUIDE.md` *(l.159)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.170)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main.py` *(l.171)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\requirements.txt` *(l.183)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\apply_optimization.py` *(l.189)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\cognitive_pipeline_hol_unified.py` *(l.190)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\INTEGRATION_MANUELLE.py` *(l.191)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\EXEMPLE_GABRIEL_v2.1.py` *(l.192)*

### `agent-multiloop-Gabriel-local\RAPPORT_ETAPE1_ANALYSE_README.md`
- **Type :** markdown
- **Taille :** 2.9 Ko
- **Modifié :** 2026-08-15 08:34:15
- **Lignes :** 142
- **Hash MD5 :** `56eac8f91c9f`
- **Références sortantes (7) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README.md` *(l.8)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` *(l.9)*
  - ❓ `ref_generique` → `README_FINAL.md` *(l.10)*
  - ❓ `ref_generique` → `README_MATHEMATICAL_v2.md` *(l.11)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md` *(l.12)*
  - ❓ `ref_generique` → `README_FOR_USER.txt` *(l.13)*
  - ❓ `ref_generique` → `README_v4.0.md` *(l.14)*

### `agent-multiloop-Gabriel-local\RAPPORT_ETAPE2_ANALYSE_ARCHITECTURE.md`
- **Type :** markdown
- **Taille :** 10.3 Ko
- **Modifié :** 2026-08-15 08:46:03
- **Lignes :** 376
- **Hash MD5 :** `a3f78b5193f7`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README.md` *(l.371)*

### `agent-multiloop-Gabriel-local\RAPPORT_MAINTENANCE_ETAPE3.md`
- **Type :** markdown
- **Taille :** 5.2 Ko
- **Modifié :** 2026-08-15 08:39:11
- **Lignes :** 198
- **Hash MD5 :** `fde92f29a072`
- **Références sortantes (7) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README.md` *(l.76)*
  - ❓ `ref_generique` → `README_FINAL.md` *(l.77)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` *(l.78)*
  - ❓ `ref_generique` → `README_MATHEMATICAL_v2.md` *(l.79)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md` *(l.80)*
  - ❓ `ref_generique` → `README_FOR_USER.txt` *(l.81)*
  - ❓ `ref_generique` → `README_v4.0.md` *(l.82)*

### `agent-multiloop-Gabriel-local\README.md`
- **Type :** markdown
- **Taille :** 13.6 Ko
- **Modifié :** 2026-08-15 08:46:58
- **Lignes :** 374
- **Hash MD5 :** `d9614e120735`
- **Références sortantes (9) :**
  - ❓ `ref_generique` → `//www.universestaucarre.com` *(l.31)*
  - ❓ `ref_generique` → `//github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026.git` *(l.38)*
  - ❓ `ref_generique` → `Emergent.sh` *(l.38)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\spectral\prime_table.py` *(l.191)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README.md` *(l.207)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` *(l.208)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md` *(l.209)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docker-compose.yml` *(l.211)*
  - ❓ `ref_generique` → `//localhost` *(l.251)*

### `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md`
- **Type :** markdown
- **Taille :** 11.5 Ko
- **Modifié :** 2026-08-15 08:36:01
- **Lignes :** 373
- **Hash MD5 :** `ee948c16ed98`
- **Références sortantes (4) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CINEMATIC_INTEGRATION_GUIDE.md` *(l.318)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CINEMATIC_MODE_SUMMARY.md` *(l.319)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md` *(l.320)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GUIDE_ANALYSE_AVEC_CRITERES.md` *(l.321)*

### `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md`
- **Type :** markdown
- **Taille :** 6.3 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 276
- **Hash MD5 :** `81df58d1132f`
- **Références sortantes (1) :**
  - ❓ `ref_generique` → `//localhost` *(l.36)*

### `agent-multiloop-Gabriel-local\RELEASE_NOTES_v2.1.md`
- **Type :** markdown
- **Taille :** 7.2 Ko
- **Modifié :** 2026-08-15 08:47:48
- **Lignes :** 281
- **Hash MD5 :** `5a328c043d74`
- **Références sortantes (9) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md` *(l.38)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README.md` *(l.39)*
  - ❓ `ref_generique` → `README_FINAL.md` *(l.43)*
  - ❓ `ref_generique` → `README_MATHEMATICAL_v2.md` *(l.43)*
  - ❓ `ref_generique` → `README_FOR_USER.txt` *(l.43)*
  - ❓ `ref_generique` → `README_v4.0.md` *(l.43)*
  - ❓ `ref_generique` → `//localhost` *(l.95)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` *(l.133)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\RAPPORT_ETAPE2_ANALYSE_ARCHITECTURE.md` *(l.141)*

### `agent-multiloop-Gabriel-local\RELEASE_v2.1_COMPLETE.txt`
- **Type :** texte
- **Taille :** 13.2 Ko
- **Modifié :** 2026-08-15 09:34:49
- **Lignes :** 319
- **Hash MD5 :** `5f5fc2a46243`
- **Références sortantes (15) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\RAPPORT_ETAPE1_ANALYSE_README.md` *(l.20)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\RAPPORT_ETAPE2_ANALYSE_ARCHITECTURE.md` *(l.26)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md` *(l.31)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\RAPPORT_MAINTENANCE_ETAPE3.md` *(l.33)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README.md` *(l.36)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\RELEASE_NOTES_v2.1.md` *(l.37)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\ETAPE5_AMELIORATIONS_PRIORITAIRES.md` *(l.46)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\image_discovery_system.py` *(l.80)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\advanced_analysis_criteria.py` *(l.87)*
  - ❓ `ref_generique` → `README_FINAL.md` *(l.93)*
  - ❓ `ref_generique` → `README_MATHEMATICAL_v2.md` *(l.94)*
  - ❓ `ref_generique` → `README_FOR_USER.txt` *(l.95)*
  - ❓ `ref_generique` → `README_v4.0.md` *(l.96)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` *(l.109)*
  - ❓ `ref_generique` → `setup.py` *(l.226)*

### `agent-multiloop-Gabriel-local\REPONSE_OUI_PREUVES_HOL4_SYSTEMATIQUES.md`
- **Type :** markdown
- **Taille :** 7.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 254
- **Hash MD5 :** `318f8087af3d`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\REPONSE_RAPIDE_RECONSTRUCTION.md`
- **Type :** markdown
- **Taille :** 1.8 Ko
- **Modifié :** 2026-08-15 08:08:28
- **Lignes :** 91
- **Hash MD5 :** `cd85cf68f167`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\RESUME_SESSION_COMPLETE.md`
- **Type :** markdown
- **Taille :** 8.3 Ko
- **Modifié :** 2026-08-15 08:20:00
- **Lignes :** 294
- **Hash MD5 :** `fc70ea61a0bc`
- **Références sortantes (5) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\gabriel_image_interface.py` *(l.91)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\image_discovery_system.py` *(l.92)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\advanced_analysis_criteria.py` *(l.93)*
  - ❓ `ref_generique` → `advanced_analysis_criteria_v2.py` *(l.94)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\validation_hol_knowledge.py` *(l.95)*

### `agent-multiloop-Gabriel-local\ROOT`
- **Type :** autre
- **Taille :** 164.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 8
- **Hash MD5 :** `5716cb3648fc`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\SECURITY_FIXES_SUMMARY.md`
- **Type :** markdown
- **Taille :** 12.0 Ko
- **Modifié :** 2026-08-15 14:59:38
- **Lignes :** 224
- **Hash MD5 :** `103d753a34dc`
- **Références sortantes (6) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\socket_cleanup.py` *(l.64)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\port_cleanup.py` *(l.78)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\engines\abstraction\abstraction_layer.py` *(l.142)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\core\llm_manager.py` *(l.143)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\tex\tex_quality\style_profile.py` *(l.147)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\tex\tex_quality\quality_pipeline.py` *(l.148)*

### `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md`
- **Type :** markdown
- **Taille :** 9.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 343
- **Hash MD5 :** `cf6c0b68190d`
- **Références sortantes (16) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\mathematical_engine.py` *(l.15)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\hol_lean_interface.py` *(l.16)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\pdf_rag_processor.py` *(l.17)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\memory\__init__.py` *(l.18)*
  - ❓ `ref_generique` → `riemann_spectral.thy` *(l.20)*
  - ❓ `ref_generique` → `pdf_index.json` *(l.26)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\gabriel_mathematical.py` *(l.27)*
  - ❓ `ref_generique` → `config_mathematical.env` *(l.28)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\requirements.txt` *(l.29)*
  - ❓ `ref_generique` → `//github.com/HOL-Theorem-Prover/HOL` *(l.51)*
  - ❓ `ref_generique` → `//raw.githubusercontent.com/leanprover/elan/master/elan-init.sh` *(l.75)*
  - ❓ `ref_generique` → `//www.wolfram.com/engine/free-license/` *(l.105)*
  - ❓ `ref_generique` → `/usr/bin/holmake` *(l.119)*
  - ❓ `ref_generique` → `/home/user/.elan/toolchains/leanprover--lean4---v4.0.0/bin` *(l.123)*
  - ❓ `ref_generique` → `/c/Users/user/.elan/toolchains/leanprover--lean4---v4.0.0/bin` *(l.124)*
  - ❓ `ref_generique` → `/opt/Wolfram/WolframKernel` *(l.131)*

### `agent-multiloop-Gabriel-local\SHORTCUTS_AND_TIPS.md`
- **Type :** markdown
- **Taille :** 5.0 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 217
- **Hash MD5 :** `09b58f3d4fc9`
- **Références sortantes (1) :**
  - ❓ `ref_generique` → `//localhost` *(l.79)*

### `agent-multiloop-Gabriel-local\SOLUTION_FINALE.txt`
- **Type :** texte
- **Taille :** 14.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 308
- **Hash MD5 :** `0935f7ec75e1`
- **Références sortantes (7) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CINEMATIC_INTEGRATION_GUIDE.md` *(l.63)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CINEMATIC_MODE_SUMMARY.md` *(l.64)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CINEMATIC_EXAMPLES.py` *(l.65)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CINEMATIC_DEPLOYMENT.md` *(l.66)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md` *(l.207)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\ui\cli.py` *(l.235)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\ui\ask_gabriel.py` *(l.235)*

### `agent-multiloop-Gabriel-local\SOLUTION_SUMMARY_v5.3.txt`
- **Type :** texte
- **Taille :** 4.2 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 175
- **Hash MD5 :** `a635c820409c`
- **Références sortantes (5) :**
  - ❓ `ref_generique` → `//localhost` *(l.27)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docker-compose.yml` *(l.31)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\gabriel_control.py` *(l.56)*
  - ❓ `ref_generique` → `/home/agent/app/theories/tex/` *(l.123)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.145)*

### `agent-multiloop-Gabriel-local\START_GABRIEL.bat`
- **Type :** autre
- **Taille :** 798.0 o
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 26
- **Hash MD5 :** `8295c25dc91e`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\START_HERE.txt`
- **Type :** texte
- **Taille :** 7.4 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 241
- **Hash MD5 :** `6bc40803506d`
- **Références sortantes (12) :**
  - ❓ `ref_generique` → `//localhost` *(l.17)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docker-compose.yml` *(l.56)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\gabriel_launcher.py` *(l.58)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` *(l.60)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_FINAL_SOLUTION.txt` *(l.64)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\QUICK_REFERENCE.md` *(l.65)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\POWERSHELL_ISE_GUIDE.md` *(l.66)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_PORT_FIX_v5.3.md` *(l.67)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PORT_CLEANUP_IMPLEMENTATION.md` *(l.68)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\port_cleanup.py` *(l.71)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\gabriel_control.py` *(l.73)*
  - ❓ `ref_generique` → `/home/agent/app/theories/tex/Geometrie_du_Spectre_des_Nombres_Premiers_2026.pdf` *(l.141)*

### `agent-multiloop-Gabriel-local\START_v5.0.txt`
- **Type :** texte
- **Taille :** 3.2 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 155
- **Hash MD5 :** `67dd48a3b8e5`
- **Références sortantes (2) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v5_EXPLIQUE_SIMPLEMENT.txt` *(l.65)*
  - ❓ `ref_generique` → `//localhost` *(l.85)*

### `agent-multiloop-Gabriel-local\STOP_GABRIEL.bat`
- **Type :** autre
- **Taille :** 722.0 o
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 24
- **Hash MD5 :** `7145988af444`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\SYNTHESE_RSA_v2.2.md`
- **Type :** markdown
- **Taille :** 6.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 288
- **Hash MD5 :** `eac102d6cbf1`
- **Références sortantes (4) :**
  - ❓ `ref_generique` → `spectral_ratio_analyzer.py` *(l.58)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\test_rsa_capability.py` *(l.63)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v2.2_RSA_CAPABILITY.md` *(l.67)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CORRECTION_RSA_v2.2.md` *(l.71)*

### `agent-multiloop-Gabriel-local\SYNTHESE_ULTIME_v2.1.md`
- **Type :** markdown
- **Taille :** 9.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 366
- **Hash MD5 :** `e08725b16dad`
- **Références sortantes (13) :**
  - ❓ `ref_generique` → `hol_proof_generator.py` *(l.15)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\hol_lean_interface.py` *(l.21)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\mathematical_engine.py` *(l.22)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\pdf_rag_processor.py` *(l.23)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\memory\__init__.py` *(l.24)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\gabriel_mathematical.py` *(l.29)*
  - ❓ `ref_generique` → `config_mathematical.env` *(l.34)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\HOL4_SYSTEMATIC_PROOFS.md` *(l.39)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v2.1_RELEASE_NOTES.md` *(l.42)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\REPONSE_OUI_PREUVES_HOL4_SYSTEMATIQUES.md` *(l.45)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\EXEMPLE_GABRIEL_v2.1.py` *(l.48)*
  - ❓ `ref_generique` → `riemann_spectral.thy` *(l.197)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\requirements.txt` *(l.329)*

### `agent-multiloop-Gabriel-local\TEMPLATES_SUMMARY.md`
- **Type :** markdown
- **Taille :** 8.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 292
- **Hash MD5 :** `483dd57f4240`
- **Références sortantes (14) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_01.thy` *(l.9)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_02.thy` *(l.10)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_100.thy` *(l.12)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docker-compose.yml` *(l.23)*
  - ❓ `ref_generique` → `./theories:/theories` *(l.25)*
  - ❓ `ref_generique` → `/theories/projects/projet_uni_car_savard_` *(l.30)*
  - ❓ `ref_generique` → `project_uni_car_savard_42.thy` *(l.112)*
  - ❓ `ref_generique` → `/theories/generated/execution_projet_42.thy` *(l.117)*
  - ❓ `ref_generique` → `/theories/projects/projet_uni_car_savard_42.thy` *(l.179)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main.py` *(l.190)*
  - ❓ `ref_generique` → `/theories/projects/` *(l.212)*
  - ❓ `ref_generique` → `/theories/projects/projet_uni_car_savard_01.thy` *(l.219)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PROJECTS_TEMPLATES_GUIDE.md` *(l.231)*
  - ❓ `ref_generique` → `//localhost` *(l.283)*

### `agent-multiloop-Gabriel-local\TODO_ANALYSE.md`
- **Type :** markdown
- **Taille :** 13.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 259
- **Hash MD5 :** `b1f0eb0b2eaa`
- **Références sortantes (12) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\cost_manager.py` *(l.59)*
  - ❓ `ref_generique` → `gabriel_llm_integration.py` *(l.60)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\gabriel_llm_integration_safe.py` *(l.61)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\hol_lean_interface.py` *(l.62)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\hol_proof_corrector.py` *(l.63)*
  - ❓ `ref_generique` → `hol_proof_generator.py` *(l.64)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\isabelle_validator.py` *(l.65)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\llm_router.py` *(l.66)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\mathematical_engine.py` *(l.67)*
  - ❓ `ref_generique` → `multiloop_validation_engine.py` *(l.68)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\pdf_rag_processor.py` *(l.69)*
  - ❓ `ref_generique` → `spectral_ratio_analyzer.py` *(l.70)*

### `agent-multiloop-Gabriel-local\UPDATE_GABRIEL_v5.ps1`
- **Type :** autre
- **Taille :** 2.3 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 67
- **Hash MD5 :** `fc01d1fcf79f`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\UTF8_ENCODING_FIX.md`
- **Type :** markdown
- **Taille :** 6.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 243
- **Hash MD5 :** `52c68461eabe`
- **Références sortantes (1) :**
  - ❓ `ref_generique` → `hashlib.sh` *(l.89)*

### `agent-multiloop-Gabriel-local\VALIDATION_HOL_INTEGRATION_COMPLETE.md`
- **Type :** markdown
- **Taille :** 3.6 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 143
- **Hash MD5 :** `54250a2f178f`
- **Références sortantes (2) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\validation_hol_unifiee.thy` *(l.34)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.73)*

### `agent-multiloop-Gabriel-local\VALIDATION_HOL_UNIFIEE_ANALYSIS.md`
- **Type :** markdown
- **Taille :** 7.3 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 218
- **Hash MD5 :** `23253f7f8d7d`
- **Références sortantes (2) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\validation_hol_unifiee.thy` *(l.1)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.91)*

### `agent-multiloop-Gabriel-local\VERIFICATION_COMPLETE_RESULTAT_FINAL.md`
- **Type :** markdown
- **Taille :** 6.2 Ko
- **Modifié :** 2026-08-15 08:18:56
- **Lignes :** 181
- **Hash MD5 :** `2fb6fbd059ce`
- **Références sortantes (4) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\FINAL_RECONSTRUCTION_SUMMARY.txt` *(l.5)*
  - ❓ `ref_generique` → `DEMARRAGE_RAPIDE.md` *(l.113)*
  - ❓ `ref_generique` → `README_GUIDES.md` *(l.114)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.136)*

### `agent-multiloop-Gabriel-local\VERIFICATION_FINALE_SYNTHESE.txt`
- **Type :** texte
- **Taille :** 11.8 Ko
- **Modifié :** 2026-08-15 08:19:33
- **Lignes :** 281
- **Hash MD5 :** `7704b80a37cb`
- **Références sortantes (46) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\FINAL_RECONSTRUCTION_SUMMARY.txt` *(l.68)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GO_QUICK_START.md` *(l.73)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\QUICK_START_5_MINUTES.md` *(l.74)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\REPONSE_RAPIDE_RECONSTRUCTION.md` *(l.75)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md` *(l.78)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_IMAGE_ANALYSIS_COMPLETE_GUIDE.md` *(l.79)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\IMAGE_ANALYSIS_ANSWER_DIRECT.md` *(l.80)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GUIDE_ANALYSE_AVEC_CRITERES.md` *(l.81)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\COMMANDES_PRATIQUES_ANALYSE.md` *(l.82)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\QUICK_START_IMAGE_ANALYSIS.md` *(l.83)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GUIDE_RECONSTRUCTION_REDEMARRAGE.md` *(l.86)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\VALIDATION_HOL_UNIFIEE_ANALYSIS.md` *(l.89)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\VALIDATION_HOL_INTEGRATION_COMPLETE.md` *(l.90)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_VISION_QUICK_START.md` *(l.93)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_VISION_MODULE_DOCUMENTATION.md` *(l.94)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_VISION_VERIFICATION_COMPLETE.md` *(l.95)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_COMPLETE_VISION_INTEGRATION.md` *(l.96)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v2.1_RELEASE_NOTES.md` *(l.99)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v2.2_RSA_CAPABILITY.md` *(l.100)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v3.0_MULTILOOP_VALIDATION.md` *(l.101)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v4.0_THEORY_MEMORY.md` *(l.102)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v5.0_LLM_ROUTING.md` *(l.103)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v5.1_SAFE_BUDGET.md` *(l.104)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v5.2_DEPLOYMENT_SUMMARY.md` *(l.105)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v5.2_HOL_FORMAL.md` *(l.106)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_v5_UPDATE_GUIDE.md` *(l.107)*
  - ❓ `ref_generique` → `README_FINAL.md` *(l.108)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` *(l.109)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md` *(l.110)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CONFIG_ENV_GUIDE.md` *(l.113)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` *(l.114)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\UTF8_ENCODING_FIX.md` *(l.115)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PYTEST_CHECKLIST.md` *(l.118)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PYTEST_EXECUTION_GUIDE.md` *(l.119)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PYTEST_INDEX.md` *(l.120)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PYTEST_LIST_COMPLETE.md` *(l.121)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PYTEST_SUMMARY.md` *(l.122)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CINEMATIC_DEPLOYMENT.md` *(l.125)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\DEPLOYMENT_CHECKLIST_v4.0.md` *(l.126)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\DEPLOYMENT_SUMMARY.md` *(l.127)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.139)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main.py` *(l.140)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\requirements.txt` *(l.155)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docker-compose.yml` *(l.157)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\RAPPORT_ANALYSE_DEPENDANCES.md` *(l.277)*
  - ✅ `ref_generique` → `PLAN_ORGANISATION.md` *(l.278)*

### `agent-multiloop-Gabriel-local\VISUAL_SUMMARY_IMAGE_ANALYSIS.txt`
- **Type :** texte
- **Taille :** 13.4 Ko
- **Modifié :** 2026-08-15 07:42:41
- **Lignes :** 267
- **Hash MD5 :** `b037b5afa0df`
- **Références sortantes (11) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\complete_vision_system.py` *(l.31)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\production_validation_system.py` *(l.32)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\image_access_manager.py` *(l.33)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\vision_module.py` *(l.34)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\advanced_vision_module.py` *(l.35)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\gabriel_image_interface.py` *(l.36)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\IMAGE_ANALYSIS_ANSWER_DIRECT.md` *(l.150)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\QUICK_START_IMAGE_ANALYSIS.md` *(l.151)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\COPIER_COLLER_DIRECT.py` *(l.154)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PATCH_IMAGE_ANALYSIS_INTEGRATION.py` *(l.155)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GABRIEL_IMAGE_ANALYSIS_COMPLETE_GUIDE.md` *(l.158)*

### `agent-multiloop-Gabriel-local\apply_image_analysis_patch.py`
- **Type :** python
- **Taille :** 7.2 Ko
- **Modifié :** 2026-08-16 20:16:43
- **Lignes :** 195
- **Hash MD5 :** `580d66295bf9`
- **Références sortantes (7) :**
  - ❓ `import_module` → `re` *(l.6)*
  - ❓ `import_module` → `sys` *(l.8)*
  - ❓ `import_module` → `pathlib` *(l.9)*
  - ❓ `import_module` → `.gabriel_vision_integration` *(l.37)*
  - ✅ `Path()` → `agent-multiloop-Gabriel-local\src\ui\cli.py` *(l.178)*
  - ❓ `chemin_litteral` → `Applique les 3 modifications à cli.py` *(l.12)*
  - ❓ `chemin_litteral` → `  2. python src/ui/cli.py` *(l.190)*

### `agent-multiloop-Gabriel-local\apply_optimization.py`
- **Type :** python
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 52
- **Hash MD5 :** `4e19174311e5`
- **Références sortantes (4) :**
  - ❓ `import_module` → `yaml` *(l.12)*
  - ❓ `import_module` → `pathlib` *(l.14)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\config.yaml` *(l.16)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\config_optimized.yaml` *(l.17)*

### `agent-multiloop-Gabriel-local\backend\multiloop_backend.py`
- **Type :** python
- **Taille :** 6.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 220
- **Hash MD5 :** `4a80426e482e`
- **Références sortantes (12) :**
  - ❓ `import_module` → `logging` *(l.6)*
  - ❓ `import_module` → `sys` *(l.8)*
  - ❓ `import_module` → `os` *(l.9)*
  - ❓ `import_module` → `asyncio` *(l.10)*
  - ❓ `import_module` → `pathlib` *(l.11)*
  - ❓ `import_module` → `typing` *(l.12)*
  - ❓ `import_module` → `json` *(l.13)*
  - ❓ `import_module` → `time` *(l.14)*
  - ❓ `import_module` → `src.multiloop_validation_engine` *(l.18)*
  - ❓ `import_module` → `src.isabelle_validator` *(l.20)*
  - ❓ `import_module` → `src.hol_proof_corrector` *(l.21)*
  - ❓ `chemin_litteral` → `data/multiloop_results/latest.json` *(l.208)*

### `agent-multiloop-Gabriel-local\clean-docker.ps1`
- **Type :** autre
- **Taille :** 5.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 141
- **Hash MD5 :** `90bd8a95e05e`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\cognitive_pipeline_hol_unified.py`
- **Type :** python
- **Taille :** 20.5 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 563
- **Hash MD5 :** `33c39ee7671c`
- **Références sortantes (11) :**
  - ❓ `import_module` → `re` *(l.27)*
  - ❓ `import_module` → `sqlite3` *(l.29)*
  - ❓ `import_module` → `json` *(l.30)*
  - ❓ `import_module` → `sys` *(l.31)*
  - ❓ `import_module` → `pathlib` *(l.32)*
  - ❓ `import_module` → `dataclasses` *(l.33)*
  - ❓ `import_module` → `typing` *(l.34)*
  - ❓ `import_module` → `enum` *(l.35)*
  - ❓ `Path()` → `/home/agent/app` *(l.445)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.446)*
  - ❓ `chemin_litteral` → `hol_unified_validation.db` *(l.447)*

### `agent-multiloop-Gabriel-local\commande-gabriel\AIDE-MEMOIRE.txt`
- **Type :** texte
- **Taille :** 9.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 187
- **Hash MD5 :** `db1b8780a101`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\commande-gabriel\README.md` *(l.180)*

### `agent-multiloop-Gabriel-local\commande-gabriel\COMMANDES.md`
- **Type :** markdown
- **Taille :** 15.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 430
- **Hash MD5 :** `d338a2a7fa75`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.10)*

### `agent-multiloop-Gabriel-local\commande-gabriel\README.md`
- **Type :** markdown
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 39
- **Hash MD5 :** `631000b39096`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\config.yaml`
- **Type :** yaml
- **Taille :** 4.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 129
- **Hash MD5 :** `ef933e8d8655`
- **Références sortantes (7) :**
  - ✅ `yaml_chemin` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.62)*
  - ❓ `yaml_chemin` → `/theories` *(l.97)*
  - ❓ `yaml_chemin` → `/workspace/corpus_actions/pdf` *(l.98)*
  - ❓ `yaml_chemin` → `/workspace/corpus_actions/tex` *(l.99)*
  - ❓ `yaml_chemin` → `/home/agent/app/data` *(l.100)*
  - ❓ `yaml_chemin` → `/opt/Isabelle2025-2` *(l.105)*
  - ❓ `yaml_chemin` → `/home/agent/app/logs` *(l.126)*

### `agent-multiloop-Gabriel-local\config_optimized.yaml`
- **Type :** yaml
- **Taille :** 1.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 47
- **Hash MD5 :** `fbd0555328d6`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\deploy_image_analysis.py`
- **Type :** python
- **Taille :** 2.9 Ko
- **Modifié :** 2026-08-16 20:17:01
- **Lignes :** 94
- **Hash MD5 :** `415e0cfad82e`
- **Références sortantes (7) :**
  - ❓ `import_module` → `subprocess` *(l.6)*
  - ❓ `import_module` → `sys` *(l.8)*
  - ❓ `import_module` → `pathlib` *(l.9)*
  - ❓ `import_module` → `src.gabriel_vision_integration` *(l.61)*
  - ✅ `Path()` → `agent-multiloop-Gabriel-local\src\gabriel_vision_integration.py` *(l.27)*
  - ✅ `Path()` → `agent-multiloop-Gabriel-local\src\ui\cli.py` *(l.38)*
  - ❓ `chemin_litteral` → `  ⚠️ Manual patching required - see COMPLETE_INTEGRATION_INSTRUCTIONS.md` *(l.50)*

### `agent-multiloop-Gabriel-local\docker-compose.yml`
- **Type :** yaml
- **Taille :** 4.3 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 152
- **Hash MD5 :** `eda290c69db4`
- **Références sortantes (1) :**
  - ❓ `yaml_chemin` → `/theories` *(l.130)*

### `agent-multiloop-Gabriel-local\docs\ARCHITECTURE_USER.md`
- **Type :** markdown
- **Taille :** 3.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 90
- **Hash MD5 :** `67a0e26e122b`
- **Références sortantes (16) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\engines\abstraction\abstraction_layer.py` *(l.12)*
  - ❓ `ref_generique` → `concept_extractor.py` *(l.12)*
  - ❓ `ref_generique` → `abstraction_rules.py` *(l.12)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\engines\generalization\generalizer.py` *(l.16)*
  - ❓ `ref_generique` → `pattern_matcher.py` *(l.16)*
  - ❓ `ref_generique` → `generalization_rules.py` *(l.16)*
  - ❓ `ref_generique` → `proof_planner.py` *(l.20)*
  - ❓ `ref_generique` → `goal_analyzer.py` *(l.20)*
  - ❓ `ref_generique` → `strategy_selector.py` *(l.20)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\engines\theorem_discovery\discovery_loop.py` *(l.24)*
  - ❓ `ref_generique` → `conjecture_generator.py` *(l.24)*
  - ❓ `ref_generique` → `conjecture_filter.py` *(l.24)*
  - ❓ `ref_generique` → `graph_builder.py` *(l.28)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\engines\concept_navigation\navigator.py` *(l.28)*
  - ❓ `ref_generique` → `query_mapper.py` *(l.28)*
  - ❓ `ref_generique` → `/theories` *(l.77)*

### `agent-multiloop-Gabriel-local\docs\CORPUS_KNOWLEDGE.md`
- **Type :** markdown
- **Taille :** 3.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 95
- **Hash MD5 :** `2d77c54edab0`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\docs\PROMPT_CACHING_IMPLEMENTATION.md`
- **Type :** markdown
- **Taille :** 10.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 368
- **Hash MD5 :** `4144293e46bf`
- **Références sortantes (8) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\prompt_cache_manager.py` *(l.284)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\gabriel_llm_integration_cache.py` *(l.285)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\llm_router_cache_extension.py` *(l.286)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\examples\example_prompt_caching.py` *(l.289)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docs\PROMPT_CACHING_IMPLEMENTATION.md` *(l.292)*
  - ❓ `ref_generique` → `//docs.anthropic.com/en/docs/build-a-Claude-app/prompt-caching` *(l.358)*
  - ❓ `ref_generique` → `//examples.com/cache-analysis` *(l.359)*
  - ❓ `ref_generique` → `//github.com/...` *(l.360)*

### `agent-multiloop-Gabriel-local\docs\analysis_notes.md`
- **Type :** markdown
- **Taille :** 634.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 29
- **Hash MD5 :** `1cc72314465a`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\docs\archive\CLAUDE_API_KEY_LOCALISATION.md`
- **Type :** markdown
- **Taille :** 6.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 267
- **Hash MD5 :** `a79121d31120`
- **Références sortantes (4) :**
  - ❓ `ref_generique` → `config_mathematical.env` *(l.29)*
  - ❓ `ref_generique` → `//console.anthropic.com/` *(l.166)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\gabriel_llm_integration_v2.py` *(l.200)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\gabriel_mathematical.py` *(l.250)*

### `agent-multiloop-Gabriel-local\docs\archive\COGNITIVE_GAP_EXTENSION.md`
- **Type :** markdown
- **Taille :** 10.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 337
- **Hash MD5 :** `9090e4337372`
- **Références sortantes (4) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.190)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\spectral\gap_cognitive_model.py` *(l.202)*
  - ❓ `ref_generique` → `gap_solver.py` *(l.204)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\spectral\gap_compute.py` *(l.206)*

### `agent-multiloop-Gabriel-local\docs\archive\CORRECTIONS_7eME_LOOP.md`
- **Type :** markdown
- **Taille :** 10.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 357
- **Hash MD5 :** `a9937be438ab`
- **Références sortantes (7) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\multiloop\refinement_loop.py` *(l.53)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\multiloop\refinement_loop_fixed.py` *(l.54)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\core\pipeline.py` *(l.56)*
  - ❓ `ref_generique` → `pipeline_fixed.py` *(l.57)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\multiloop\slowmotion_trigger.py` *(l.89)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.278)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\memory\__init__.py` *(l.310)*

### `agent-multiloop-Gabriel-local\docs\archive\CORRECTION_TYPO_CLAUDE_KEY.md`
- **Type :** markdown
- **Taille :** 3.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 162
- **Hash MD5 :** `e87e47721a62`
- **Références sortantes (2) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\gabriel_mathematical.py` *(l.118)*
  - ❓ `ref_generique` → `test_claude_api_key_location.py` *(l.137)*

### `agent-multiloop-Gabriel-local\docs\archive\FIX_NEGATIVE_NUMBERS.md`
- **Type :** markdown
- **Taille :** 3.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 139
- **Hash MD5 :** `fce96dbbdb05`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\multiloop\request_decomposer.py` *(l.63)*

### `agent-multiloop-Gabriel-local\docs\archive\GABRIEL_v6.0_CLAUDE_PRIORITAIRE.md`
- **Type :** markdown
- **Taille :** 8.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 377
- **Hash MD5 :** `8979bc75f772`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\docs\archive\GABRIEL_v6.0_EXECUTIVE_SUMMARY.md`
- **Type :** markdown
- **Taille :** 8.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 340
- **Hash MD5 :** `35e39c029d3c`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `deploy_gabriel_v6.py` *(l.219)*

### `agent-multiloop-Gabriel-local\docs\archive\GABRIEL_v6.0_QUICK_REFERENCE.md`
- **Type :** markdown
- **Taille :** 5.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 291
- **Hash MD5 :** `18e987f4a000`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `deploy_gabriel_v6.py` *(l.221)*

### `agent-multiloop-Gabriel-local\docs\archive\GABRIEL_v6.1_GAP_MIXED_HOL4.md`
- **Type :** markdown
- **Taille :** 9.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 365
- **Hash MD5 :** `2a51123a9f48`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\gabriel_llm_integration_v2.py` *(l.309)*

### `agent-multiloop-Gabriel-local\docs\archive\GABRIEL_v6.2_RAG_SEMANTIQUE.md`
- **Type :** markdown
- **Taille :** 8.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 336
- **Hash MD5 :** `3c0093122e2c`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\docs\archive\GAP_DEPLOYMENT.md`
- **Type :** markdown
- **Taille :** 12.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 364
- **Hash MD5 :** `a3ae6e90fb83`
- **Références sortantes (5) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\spectral\gap_cognitive_model.py` *(l.8)*
  - ❓ `ref_generique` → `gap_solver.py` *(l.9)*
  - ❓ `ref_generique` → `/theories` *(l.58)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.283)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docs\archive\COGNITIVE_GAP_EXTENSION.md` *(l.315)*

### `agent-multiloop-Gabriel-local\docs\archive\GAP_FORMULA_CORRECTION.md`
- **Type :** markdown
- **Taille :** 6.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 256
- **Hash MD5 :** `661573baec16`
- **Références sortantes (2) :**
  - ❓ `ref_generique` → `gap_solver.py` *(l.5)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\spectral\gap_solver_corrected.py` *(l.230)*

### `agent-multiloop-Gabriel-local\docs\archive\LLM_MANAGER_v2_MIGRATION.md`
- **Type :** markdown
- **Taille :** 7.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 267
- **Hash MD5 :** `0e60468f2e64`
- **Références sortantes (1) :**
  - ❓ `ref_generique` → `//localhost` *(l.113)*

### `agent-multiloop-Gabriel-local\docs\archive\META_LEARNING_EXPERTISE.md`
- **Type :** markdown
- **Taille :** 14.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 479
- **Hash MD5 :** `6111e90b8ab2`
- **Références sortantes (7) :**
  - ❓ `ref_generique` → `MetaLearningManager.sh` *(l.156)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\learning\debugging_expertise.py` *(l.281)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\learning\slowmotion_recorder.py` *(l.282)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\learning\meta_learning_integration.py` *(l.283)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\memory\__init__.py` *(l.453)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\core\pipeline.py` *(l.456)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\ui\cli.py` *(l.456)*

### `agent-multiloop-Gabriel-local\docs\archive\SECURITY_FIX.md`
- **Type :** markdown
- **Taille :** 8.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 366
- **Hash MD5 :** `92dff39d014c`
- **Références sortantes (8) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docs\archive\SECURITY_FIX.md` *(l.1)*
  - ❓ `ref_generique` → `//platform.openai.com/api-keys` *(l.20)*
  - ❓ `ref_generique` → `non-.env` *(l.69)*
  - ❓ `ref_generique` → `./backup` *(l.70)*
  - ❓ `ref_generique` → `//www.gitguardian.com/` *(l.189)*
  - ❓ `ref_generique` → `/path/to/repo` *(l.194)*
  - ❓ `ref_generique` → `//github.com/2racinede4carreunivers-dev/...` *(l.222)*
  - ❓ `ref_generique` → `//api.github.com/repos/.../.../contents/.env` *(l.355)*

### `agent-multiloop-Gabriel-local\docs\archive\SECURITY_GUIDE.md`
- **Type :** markdown
- **Taille :** 8.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 406
- **Hash MD5 :** `67dbe271dac1`
- **Références sortantes (8) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docs\archive\SECURITY_GUIDE.md` *(l.1)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docs\archive\SECURITY_FIX.md` *(l.9)*
  - ❓ `ref_generique` → `//platform.openai.com/api-keys` *(l.20)*
  - ✅ `ref_generique` → `security_validator.py` *(l.39)*
  - ❓ `ref_generique` → `//platform.openai.com/account/usage` *(l.137)*
  - ❓ `ref_generique` → `//github.com/settings/tokens` *(l.142)*
  - ❓ `ref_generique` → `//github.com/settings/security-log` *(l.328)*
  - ❓ `ref_generique` → `//api.github.com/.../contents/.env` *(l.353)*

### `agent-multiloop-Gabriel-local\docs\archive\SETUP_FINAL.md`
- **Type :** markdown
- **Taille :** 7.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 142
- **Hash MD5 :** `7f67b53b9107`
- **Références sortantes (5) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docker-compose.yml` *(l.29)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\config.yaml` *(l.30)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.33)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main.py` *(l.53)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\requirements.txt` *(l.55)*

### `agent-multiloop-Gabriel-local\docs\archive\SOLUTION_DEFINITIVE.md`
- **Type :** markdown
- **Taille :** 3.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 132
- **Hash MD5 :** `13b92d64fa74`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\docs\archive\SYNTHESE_COMPLETE.md`
- **Type :** markdown
- **Taille :** 15.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 405
- **Hash MD5 :** `526a3c83be9f`
- **Références sortantes (13) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\multiloop\refinement_loop_fixed.py` *(l.17)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\multiloop\slowmotion_trigger.py` *(l.21)*
  - ❓ `ref_generique` → `pipeline_fixed.py` *(l.25)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\learning\debugging_expertise.py` *(l.33)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\learning\slowmotion_recorder.py` *(l.41)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\learning\meta_learning_integration.py` *(l.48)*
  - ❓ `ref_generique` → `dbg_a1b2c3d4.json` *(l.60)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\multiloop\refinement_loop.py` *(l.184)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\core\pipeline.py` *(l.186)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\memory\__init__.py` *(l.193)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docs\archive\CORRECTIONS_7eME_LOOP.md` *(l.202)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docs\archive\META_LEARNING_EXPERTISE.md` *(l.203)*
  - ❓ `ref_generique` → `Pipeline_fixed.py` *(l.267)*

### `agent-multiloop-Gabriel-local\docs\archive\test_result.md`
- **Type :** markdown
- **Taille :** 4.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 103
- **Hash MD5 :** `260454560649`
- **Références sortantes (3) :**
  - ❓ `ref_generique` → `file_path.py` *(l.22)*
  - ❓ `ref_generique` → `task_result.md` *(l.76)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docs\archive\test_result.md` *(l.91)*

### `agent-multiloop-Gabriel-local\docs\geometrie_spectre_premiers.docx`
- **Type :** autre
- **Taille :** 27.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Hash MD5 :** `d7795e9973e4`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\docs\geometrie_spectre_premiers.tex`
- **Type :** latex
- **Taille :** 38.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 589
- **Hash MD5 :** `d2d031be344b`
- **Références sortantes (11) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.12)*
  - ❓ `latex_inclusion` → `fontenc` *(l.13)*
  - ❓ `latex_inclusion` → `babel` *(l.14)*
  - ❓ `latex_inclusion` → `lmodern` *(l.15)*
  - ❓ `latex_inclusion` → `amsmath, amssymb, amsthm` *(l.16)*
  - ❓ `latex_inclusion` → `graphicx` *(l.17)*
  - ❓ `latex_inclusion` → `booktabs, longtable, array` *(l.18)*
  - ❓ `latex_inclusion` → `hyperref` *(l.19)*
  - ❓ `latex_inclusion` → `xcolor` *(l.20)*
  - ❓ `latex_inclusion` → `geometry` *(l.21)*
  - ❓ `latex_inclusion` → `fancyhdr` *(l.22)*

### `agent-multiloop-Gabriel-local\docs\psi_savard_comparison.tex`
- **Type :** latex
- **Taille :** 2.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 49
- **Hash MD5 :** `c4d8a8f93cd6`
- **Références sortantes (4) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.2)*
  - ❓ `latex_inclusion` → `fontenc` *(l.3)*
  - ❓ `latex_inclusion` → `babel` *(l.4)*
  - ❓ `latex_inclusion` → `amsmath,amssymb,booktabs,pgfplots` *(l.5)*

### `agent-multiloop-Gabriel-local\env.example.txt`
- **Type :** texte
- **Taille :** 1.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 38
- **Hash MD5 :** `7978b2c04757`
- **Références sortantes (6) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\env.example.txt` *(l.6)*
  - ❓ `ref_generique` → `//developer.wolframalpha.com/access` *(l.14)*
  - ❓ `ref_generique` → `//host.docker.internal` *(l.19)*
  - ❓ `ref_generique` → `/theories` *(l.27)*
  - ❓ `ref_generique` → `/workspace/corpus_actions/pdf` *(l.28)*
  - ❓ `ref_generique` → `/workspace/corpus_actions/tex` *(l.29)*

### `agent-multiloop-Gabriel-local\examples\example_prompt_caching.py`
- **Type :** python
- **Taille :** 10.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 295
- **Hash MD5 :** `c8876c932c88`
- **Références sortantes (6) :**
  - ❓ `import_module` → `logging` *(l.6)*
  - ❓ `import_module` → `pathlib` *(l.8)*
  - ❓ `import_module` → `sys` *(l.9)*
  - ❓ `import_module` → `src.prompt_cache_manager` *(l.15)*
  - ❓ `import_module` → `src.gabriel_llm_integration_cache` *(l.17)*
  - ❓ `import_module` → `traceback` *(l.257)*

### `agent-multiloop-Gabriel-local\examples\verif_p103_n27_CORRECT.thy`
- **Type :** isabelle
- **Taille :** 1.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 44
- **Hash MD5 :** `7c8426cde961`
- **Références sortantes (1) :**
  - ✅ `thy_import` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.1)*

### `agent-multiloop-Gabriel-local\examples\verif_p59_n17_CORRECTED.thy`
- **Type :** isabelle
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 46
- **Hash MD5 :** `21c6bbe4ea2c`
- **Références sortantes (1) :**
  - ✅ `thy_import` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.1)*

### `agent-multiloop-Gabriel-local\gabriel.ps1`
- **Type :** autre
- **Taille :** 6.0 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 210
- **Hash MD5 :** `40fa4036d0b7`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\gabriel_control.py`
- **Type :** python
- **Taille :** 3.6 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 125
- **Hash MD5 :** `f6abec983b47`
- **Références sortantes (4) :**
  - ❓ `import_module` → `subprocess` *(l.6)*
  - ❓ `import_module` → `sys` *(l.8)*
  - ❓ `import_module` → `time` *(l.9)*
  - ❓ `import_module` → `logging` *(l.10)*

### `agent-multiloop-Gabriel-local\gabriel_launcher.py`
- **Type :** python
- **Taille :** 2.0 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 65
- **Hash MD5 :** `05def9b8550a`
- **Références sortantes (8) :**
  - ❓ `import_module` → `os` *(l.6)*
  - ❓ `import_module` → `sys` *(l.8)*
  - ❓ `import_module` → `logging` *(l.9)*
  - ❓ `import_module` → `pathlib` *(l.10)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\port_cleanup.py` *(l.18)*
  - ❓ `import_module` → `src.core.logging_setup` *(l.31)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.51)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\logs` *(l.32)*

### `agent-multiloop-Gabriel-local\gabriel_mathematical.py`
- **Type :** python
- **Taille :** 17.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 449
- **Hash MD5 :** `deccd105228e`
- **Références sortantes (13) :**
  - ❓ `import_module` → `logging` *(l.5)*
  - ❓ `import_module` → `os` *(l.7)*
  - ❓ `import_module` → `pathlib` *(l.8)*
  - ❓ `import_module` → `typing` *(l.9)*
  - ❓ `import_module` → `dataclasses` *(l.10)*
  - ❓ `import_module` → `dotenv` *(l.11)*
  - ❓ `import_module` → `src.mathematical_engine` *(l.15)*
  - ❓ `import_module` → `src.hol_lean_interface` *(l.16)*
  - ❓ `import_module` → `src.pdf_rag_processor` *(l.21)*
  - ❓ `import_module` → `src.hol_proof_generator` *(l.22)*
  - ❓ `import_module` → `src.spectral_ratio_analyzer` *(l.23)*
  - ❓ `import_module` → `re` *(l.200)*
  - ❓ `chemin_litteral` → `config_mathematical.env` *(l.37)*

### `agent-multiloop-Gabriel-local\generate_thy_templates.py`
- **Type :** python
- **Taille :** 3.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 115
- **Hash MD5 :** `6ed9912e380b`
- **Références sortantes (7) :**
  - ❓ `import_module` → `pathlib` *(l.8)*
  - ❓ `chemin_litteral` → `{project_name}.thy` *(l.75)*
  - ❓ `chemin_litteral` → `  - projet_uni_car_savard_001.thy` *(l.101)*
  - ❓ `chemin_litteral` → `  - projet_uni_car_savard_002.thy` *(l.102)*
  - ❓ `chemin_litteral` → `  - projet_uni_car_savard_100.thy` *(l.104)*
  - ❓ `chemin_litteral` → `  - /theories/projects/projet_uni_car_savard_001.thy` *(l.109)*
  - ❓ `chemin_litteral` → `  - /theories/projects/projet_uni_car_savard_002.thy` *(l.110)*

### `agent-multiloop-Gabriel-local\generate_txt_tex_templates.py`
- **Type :** python
- **Taille :** 6.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 218
- **Hash MD5 :** `20a2e72e5fdb`
- **Références sortantes (4) :**
  - ❓ `import_module` → `pathlib` *(l.8)*
  - ❓ `chemin_litteral` → `{project_name}.txt` *(l.149)*
  - ❓ `chemin_litteral` → `  ├── projet_uni_car_savard_*.thy` *(l.214)*
  - ❓ `chemin_litteral` → `  ├── txt/projet_uni_car_savard_*.txt` *(l.215)*

### `agent-multiloop-Gabriel-local\guide_utilisateur\01_DEMARRAGE_RAPIDE\INDEX.md`
- **Type :** markdown
- **Taille :** 106.0 o
- **Modifié :** 2026-08-15 12:46:40
- **Lignes :** 4
- **Hash MD5 :** `ef3f8198f463`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\guide_utilisateur\02_MODE_CINEMATIQUE\INDEX.md`
- **Type :** markdown
- **Taille :** 288.0 o
- **Modifié :** 2026-08-15 12:46:44
- **Lignes :** 11
- **Hash MD5 :** `4bbc656fbdd4`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\guide_utilisateur\03_ANALYSE_IMAGES\INDEX.md`
- **Type :** markdown
- **Taille :** 422.0 o
- **Modifié :** 2026-08-15 12:46:51
- **Lignes :** 13
- **Hash MD5 :** `a38613ae8518`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\guide_utilisateur\04_DEPLOIEMENT\INDEX.md`
- **Type :** markdown
- **Taille :** 415.0 o
- **Modifié :** 2026-08-15 12:47:00
- **Lignes :** 14
- **Hash MD5 :** `33bc0deedff7`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\guide_utilisateur\05_MATHEMATIQUES\INDEX.md`
- **Type :** markdown
- **Taille :** 479.0 o
- **Modifié :** 2026-08-15 12:47:09
- **Lignes :** 16
- **Hash MD5 :** `6ca17619d054`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\guide_utilisateur\06_RECONSTRUCTION\INDEX.md`
- **Type :** markdown
- **Taille :** 352.0 o
- **Modifié :** 2026-08-15 12:47:15
- **Lignes :** 12
- **Hash MD5 :** `a04b1a696dbc`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\guide_utilisateur\07_TESTS_VALIDATION\INDEX.md`
- **Type :** markdown
- **Taille :** 484.0 o
- **Modifié :** 2026-08-15 12:47:22
- **Lignes :** 17
- **Hash MD5 :** `1bc7fb7b8c63`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\guide_utilisateur\08_CONFIGURATION\INDEX.md`
- **Type :** markdown
- **Taille :** 485.0 o
- **Modifié :** 2026-08-15 12:47:28
- **Lignes :** 16
- **Hash MD5 :** `7afb9037b9ce`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\guide_utilisateur\09_COMMANDES_REFERENCES\INDEX.md`
- **Type :** markdown
- **Taille :** 454.0 o
- **Modifié :** 2026-08-15 12:47:33
- **Lignes :** 14
- **Hash MD5 :** `08d1866df3fb`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\guide_utilisateur\10_RAPPORTS_ANALYSES\INDEX.md`
- **Type :** markdown
- **Taille :** 479.0 o
- **Modifié :** 2026-08-15 12:47:42
- **Lignes :** 14
- **Hash MD5 :** `52b1c4fe4c0e`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\guide_utilisateur\11_VERSIONS_RELEASES\INDEX.md`
- **Type :** markdown
- **Taille :** 519.0 o
- **Modifié :** 2026-08-15 12:47:50
- **Lignes :** 13
- **Hash MD5 :** `32d705362058`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\guide_utilisateur\README.md`
- **Type :** markdown
- **Taille :** 4.5 Ko
- **Modifié :** 2026-08-15 12:46:37
- **Lignes :** 134
- **Hash MD5 :** `c675f62550b5`
- **Références sortantes (7) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\QUICK_START_5_MINUTES.md` *(l.111)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README_CINEMATIC_MODE.md` *(l.112)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\GUIDE_COMPLET_ANALYSE_IMAGES_SCHEMAS_FIGURES.md` *(l.113)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\README_FINAL_v5.4.md` *(l.114)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\PYTEST_SUMMARY.md` *(l.115)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\COMMANDS_COMPLETE_REFERENCE.md` *(l.116)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CONFIG_ENV_GUIDE.md` *(l.117)*

### `agent-multiloop-Gabriel-local\integration_mathematical.py`
- **Type :** python
- **Taille :** 8.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 247
- **Hash MD5 :** `8fdf99f5f1db`
- **Références sortantes (8) :**
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\gabriel_mathematical.py` *(l.9)*
  - ❓ `import_module` → `fastapi` *(l.91)*
  - ❓ `import_module` → `pydantic` *(l.93)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\integration_mathematical.py` *(l.177)*
  - ❓ `import_module` → `uvicorn` *(l.194)*
  - ❓ `import_module` → `asyncio` *(l.245)*
  - ❓ `chemin_litteral` → `/api/mathematical/query` *(l.103)*
  - ❓ `chemin_litteral` → `/api/mathematical/capabilities` *(l.144)*

### `agent-multiloop-Gabriel-local\lakefile.lean`
- **Type :** autre
- **Taille :** 460.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 19
- **Hash MD5 :** `b2cc751ba7ae`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\lean-toolchain`
- **Type :** autre
- **Taille :** 26.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 2
- **Hash MD5 :** `5091aab81b19`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\main.py`
- **Type :** python
- **Taille :** 3.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 131
- **Hash MD5 :** `819db3709d96`
- **Références sortantes (16) :**
  - ❓ `import_module` → `__future__` *(l.3)*
  - ❓ `import_module` → `logging` *(l.4)*
  - ❓ `import_module` → `os` *(l.6)*
  - ❓ `import_module` → `sys` *(l.7)*
  - ❓ `import_module` → `time` *(l.8)*
  - ❓ `import_module` → `pathlib` *(l.9)*
  - ❓ `import_module` → `src.core.config` *(l.15)*
  - ❓ `import_module` → `src.core.logging_setup` *(l.17)*
  - ❓ `import_module` → `rich.console` *(l.23)*
  - ❓ `import_module` → `rich.panel` *(l.24)*
  - ❓ `import_module` → `rich.text` *(l.25)*
  - ❓ `import_module` → `rich.align` *(l.26)*
  - ❓ `import_module` → `rich.box` *(l.27)*
  - ❓ `import_module` → `src.ui.cli` *(l.111)*
  - ❓ `import_module` → `src.core.scientific_badge` *(l.115)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\logs` *(l.102)*

### `agent-multiloop-Gabriel-local\main_cli.py`
- **Type :** python
- **Taille :** 6.3 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 206
- **Hash MD5 :** `e852533b2676`
- **Références sortantes (21) :**
  - ❓ `import_module` → `__future__` *(l.12)*
  - ❓ `import_module` → `asyncio` *(l.13)*
  - ❓ `import_module` → `logging` *(l.15)*
  - ❓ `import_module` → `os` *(l.16)*
  - ❓ `import_module` → `sys` *(l.17)*
  - ❓ `import_module` → `threading` *(l.18)*
  - ❓ `import_module` → `time` *(l.19)*
  - ❓ `import_module` → `concurrent.futures` *(l.20)*
  - ❓ `import_module` → `pathlib` *(l.21)*
  - ❓ `import_module` → `src.core.config` *(l.27)*
  - ❓ `import_module` → `src.core.logging_setup` *(l.29)*
  - ❓ `import_module` → `src.core.pipeline` *(l.30)*
  - ❓ `import_module` → `rich.console` *(l.38)*
  - ❓ `import_module` → `rich.panel` *(l.39)*
  - ❓ `import_module` → `rich.text` *(l.40)*
  - ❓ `import_module` → `rich.align` *(l.41)*
  - ❓ `import_module` → `rich.box` *(l.42)*
  - ❓ `import_module` → `src.api.gabriel_http_api` *(l.109)*
  - ❓ `import_module` → `src.ui.cli` *(l.121)*
  - ❓ `import_module` → `src.core.scientific_badge` *(l.162)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\logs` *(l.136)*

### `agent-multiloop-Gabriel-local\memory\__init__.py`
- **Type :** python
- **Taille :** 749.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 28
- **Hash MD5 :** `d3ad6204c285`
- **Références sortantes (3) :**
  - ❓ `import_module` → `__future__` *(l.7)*
  - ❓ `import_module` → `.dictionnaire_spectral` *(l.8)*
  - ❓ `import_module` → `.adaptateur_cognitif_rag` *(l.15)*

### `agent-multiloop-Gabriel-local\memory\adaptateur_cognitif_rag.py`
- **Type :** python
- **Taille :** 7.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 196
- **Hash MD5 :** `ea6e716d5c9f`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.12)*
  - ❓ `import_module` → `logging` *(l.13)*
  - ❓ `import_module` → `re` *(l.15)*
  - ❓ `import_module` → `dataclasses` *(l.16)*
  - ❓ `import_module` → `typing` *(l.17)*
  - ❓ `import_module` → `.dictionnaire_spectral` *(l.18)*

### `agent-multiloop-Gabriel-local\memory\banque_qr_methode_spectrale.md`
- **Type :** markdown
- **Taille :** 13.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 265
- **Hash MD5 :** `c40cbf0af838`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\memory\dictionnaire_spectral.py`
- **Type :** python
- **Taille :** 38.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 755
- **Hash MD5 :** `9300bd80299b`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.17)*
  - ❓ `import_module` → `dataclasses` *(l.18)*
  - ❓ `import_module` → `fractions` *(l.20)*
  - ❓ `import_module` → `typing` *(l.21)*

### `agent-multiloop-Gabriel-local\memory\methode_spectral_section_XI.py`
- **Type :** python
- **Taille :** 3.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 104
- **Hash MD5 :** `6c9814cfa407`
- **Références sortantes (3) :**
  - ❓ `import_module` → `__future__` *(l.10)*
  - ❓ `import_module` → `typing` *(l.11)*
  - ❓ `chemin_litteral` → `methode_spectral_section_XI.thy` *(l.84)*

### `agent-multiloop-Gabriel-local\memory\methode_spectral_section_XII.py`
- **Type :** python
- **Taille :** 9.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 260
- **Hash MD5 :** `86732de4ac32`
- **Références sortantes (3) :**
  - ❓ `import_module` → `__future__` *(l.16)*
  - ❓ `import_module` → `fractions` *(l.17)*
  - ❓ `import_module` → `typing` *(l.18)*

### `agent-multiloop-Gabriel-local\memory\methode_spectral_section_XIII.py`
- **Type :** python
- **Taille :** 19.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 419
- **Hash MD5 :** `e20547fb4117`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.25)*
  - ❓ `import_module` → `math` *(l.26)*
  - ❓ `import_module` → `typing` *(l.28)*
  - ❓ `import_module` → `src.spectral.spectral_ratio` *(l.381)*

### `agent-multiloop-Gabriel-local\memory\prompt_injector_enhanced.py`
- **Type :** python
- **Taille :** 8.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 244
- **Hash MD5 :** `34ba80287f0d`
- **Références sortantes (5) :**
  - ❓ `import_module` → `__future__` *(l.9)*
  - ❓ `import_module` → `logging` *(l.10)*
  - ❓ `import_module` → `re` *(l.12)*
  - ❓ `import_module` → `dataclasses` *(l.13)*
  - ❓ `import_module` → `typing` *(l.14)*

### `agent-multiloop-Gabriel-local\port-locker.ps1`
- **Type :** autre
- **Taille :** 2.3 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 76
- **Hash MD5 :** `448ac60ca1e8`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\port_cleanup.py`
- **Type :** python
- **Taille :** 7.8 Ko
- **Modifié :** 2026-08-15 14:54:30
- **Lignes :** 204
- **Hash MD5 :** `230976dce2fe`
- **Références sortantes (10) :**
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\port_cleanup.py` *(l.10)*
  - ❓ `import_module` → `os` *(l.17)*
  - ❓ `import_module` → `socket` *(l.19)*
  - ❓ `import_module` → `signal` *(l.20)*
  - ❓ `import_module` → `sys` *(l.21)*
  - ❓ `import_module` → `logging` *(l.22)*
  - ❓ `import_module` → `time` *(l.23)*
  - ❓ `import_module` → `contextlib` *(l.24)*
  - ❓ `import_module` → `pathlib` *(l.25)*
  - ❓ `import_module` → `subprocess` *(l.108)*

### `agent-multiloop-Gabriel-local\question-definition.txt`
- **Type :** texte
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 11
- **Hash MD5 :** `e827bc5077d8`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.1)*

### `agent-multiloop-Gabriel-local\quick-start.sh`
- **Type :** shell
- **Taille :** 4.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 127
- **Hash MD5 :** `6ffdf75f486b`
- **Références sortantes (2) :**
  - ❓ `shell_appel` → `Please` *(l.21)*
  - ❓ `shell_appel` → `Trying` *(l.25)*

### `agent-multiloop-Gabriel-local\quick_verification.py`
- **Type :** python
- **Taille :** 6.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 192
- **Hash MD5 :** `9076b511cb32`
- **Références sortantes (17) :**
  - ❓ `import_module` → `os` *(l.7)*
  - ❓ `import_module` → `sys` *(l.9)*
  - ❓ `import_module` → `pathlib` *(l.10)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\src\mathematical_engine.py` *(l.45)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\src\hol_lean_interface.py` *(l.46)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\src\pdf_rag_processor.py` *(l.47)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\src\__init__.py` *(l.48)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\gabriel_mathematical.py` *(l.49)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\integration_mathematical.py` *(l.50)*
  - ❓ `chemin_litteral` → `config_mathematical.env` *(l.51)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\requirements.txt` *(l.52)*
  - ❓ `chemin_litteral` → `theories/riemann_spectral.thy` *(l.53)*
  - ❓ `chemin_litteral` → `README_MATHEMATICAL_v2.md` *(l.55)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\SETUP_MATHEMATICAL_v2.md` *(l.56)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\CHECKLIST_FINAL.md` *(l.57)*
  - ❓ `chemin_litteral` → `  1. pip install -r requirements.txt` *(l.173)*
  - ❓ `chemin_litteral` → `\n[INFO] Consulter: SETUP_MATHEMATICAL_v2.md` *(l.187)*

### `agent-multiloop-Gabriel-local\requirements.txt`
- **Type :** texte
- **Taille :** 2.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 84
- **Hash MD5 :** `209cc974a137`
- **Références sortantes (1) :**
  - ❓ `ref_generique` → `SETUP.md` *(l.55)*

### `agent-multiloop-Gabriel-local\run-tests.bat`
- **Type :** autre
- **Taille :** 1.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 69
- **Hash MD5 :** `cef7ff680ce1`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\run-tests.ps1`
- **Type :** autre
- **Taille :** 3.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 90
- **Hash MD5 :** `5c6b02aada60`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\scripts\healthcheck_tex.sh`
- **Type :** shell
- **Taille :** 6.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 163
- **Hash MD5 :** `5d73ce3603c3`
- **Références sortantes (7) :**
  - ❓ `shell_appel` → `-` *(l.3)*
  - ❓ `shell_appel` → `path/to/file.tex` *(l.18)*
  - ❓ `shell_appel` → `.git/hooks/pre-commit` *(l.21)*
  - ❓ `shell_appel` → `if` *(l.35)*
  - ❓ `shell_appel` → `def` *(l.82)*
  - ❓ `shell_appel` → `starred_secs` *(l.104)*
  - ❓ `shell_appel` → `Compilation` *(l.156)*

### `agent-multiloop-Gabriel-local\scripts\isabelle-integration.sh`
- **Type :** shell
- **Taille :** 3.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 113
- **Hash MD5 :** `3dd9f02f7a1b`
- **Références sortantes (4) :**
  - ❓ `shell_appel` → `Surveille` *(l.7)*
  - ❓ `shell_appel` → `Traite` *(l.8)*
  - ❓ `shell_appel` → `Envoie` *(l.9)*
  - ❓ `shell_appel` → `Sauvegarde` *(l.10)*

### `agent-multiloop-Gabriel-local\scripts\isabelle_static_check.py`
- **Type :** python
- **Taille :** 7.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 196
- **Hash MD5 :** `74fa51b4a1da`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.15)*
  - ❓ `import_module` → `re` *(l.16)*
  - ❓ `import_module` → `sys` *(l.17)*
  - ❓ `import_module` → `collections` *(l.18)*
  - ❓ `import_module` → `pathlib` *(l.19)*
  - ❓ `chemin_litteral` → `theories/methode_spectral.thy` *(l.21)*

### `agent-multiloop-Gabriel-local\scripts\sync_theory_to_agent.py`
- **Type :** python
- **Taille :** 8.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 233
- **Hash MD5 :** `7ceaf57d07ea`
- **Références sortantes (14) :**
  - ❓ `import_module` → `__future__` *(l.16)*
  - ❓ `import_module` → `argparse` *(l.17)*
  - ❓ `import_module` → `importlib` *(l.18)*
  - ❓ `import_module` → `subprocess` *(l.19)*
  - ❓ `import_module` → `sys` *(l.20)*
  - ❓ `import_module` → `pathlib` *(l.21)*
  - ❓ `import_module` → `memory.dictionnaire_spectral` *(l.74)*
  - ❓ `import_module` → `memory.methode_spectral_section_XI` *(l.99)*
  - ❓ `import_module` → `memory.methode_spectral_section_XII` *(l.107)*
  - ❓ `import_module` → `fractions` *(l.116)*
  - ❓ `import_module` → `memory.methode_spectral_section_XIII` *(l.137)*
  - ❓ `import_module` → `memory.adaptateur_cognitif_rag` *(l.162)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.24)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\scripts\isabelle_static_check.py` *(l.25)*

### `agent-multiloop-Gabriel-local\scripts\tex_healthcheck.py`
- **Type :** python
- **Taille :** 5.6 Ko
- **Modifié :** 2026-08-07 09:31:46
- **Lignes :** 188
- **Hash MD5 :** `9fa2ed28d2f3`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.7)*
  - ❓ `import_module` → `argparse` *(l.9)*
  - ❓ `import_module` → `re` *(l.11)*
  - ❓ `import_module` → `shutil` *(l.12)*
  - ❓ `import_module` → `subprocess` *(l.13)*
  - ❓ `import_module` → `sys` *(l.14)*
  - ❓ `import_module` → `pathlib` *(l.15)*

### `agent-multiloop-Gabriel-local\scripts\translate_thy.py`
- **Type :** python
- **Taille :** 21.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 547
- **Hash MD5 :** `cfa3e047ce64`
- **Références sortantes (13) :**
  - ❓ `import_module` → `__future__` *(l.16)*
  - ❓ `import_module` → `asyncio` *(l.17)*
  - ❓ `import_module` → `json` *(l.19)*
  - ❓ `import_module` → `os` *(l.20)*
  - ❓ `import_module` → `re` *(l.21)*
  - ❓ `import_module` → `sys` *(l.22)*
  - ❓ `import_module` → `pathlib` *(l.23)*
  - ❓ `import_module` → `typing` *(l.24)*
  - ❓ `import_module` → `emergentintegrations.llm.chat` *(l.25)*
  - ❓ `import_module` → `json5` *(l.348)*
  - ❓ `Path()` → `theories/methode_spectral.thy` *(l.32)*
  - ❓ `Path()` → `theories` *(l.33)*
  - ❓ `chemin_litteral` → `methode_spectral_{lang_code}.thy` *(l.519)*

### `agent-multiloop-Gabriel-local\socket_cleanup.py`
- **Type :** python
- **Taille :** 8.5 Ko
- **Modifié :** 2026-08-15 14:52:32
- **Lignes :** 229
- **Hash MD5 :** `fd63cf1b67ac`
- **Références sortantes (8) :**
  - ❓ `import_module` → `os` *(l.11)*
  - ❓ `import_module` → `sys` *(l.13)*
  - ❓ `import_module` → `socket` *(l.14)*
  - ❓ `import_module` → `logging` *(l.15)*
  - ❓ `import_module` → `subprocess` *(l.16)*
  - ❓ `import_module` → `time` *(l.17)*
  - ❓ `import_module` → `typing` *(l.18)*
  - ❓ `import_module` → `contextlib` *(l.19)*

### `agent-multiloop-Gabriel-local\src\.gitkeep`
- **Type :** autre
- **Taille :** 0.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 1
- **Hash MD5 :** `d41d8cd98f00`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\src\__init__.py`
- **Type :** python
- **Taille :** 756.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 38
- **Hash MD5 :** `8d2a1e9be43c`
- **Références sortantes (3) :**
  - ❓ `import_module` → `.mathematical_engine` *(l.5)*
  - ❓ `import_module` → `.hol_lean_interface` *(l.10)*
  - ❓ `import_module` → `.pdf_rag_processor` *(l.17)*

### `agent-multiloop-Gabriel-local\src\adapters\__init__.py`
- **Type :** python
- **Taille :** 25.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 2
- **Hash MD5 :** `3176ae355e99`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\src\adapters\corpus\__init__.py`
- **Type :** python
- **Taille :** 100.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 5
- **Hash MD5 :** `95d7504b8e4f`
- **Références sortantes (1) :**
  - ❓ `import_module` → `.thy_loader` *(l.2)*

### `agent-multiloop-Gabriel-local\src\adapters\corpus\certainty_kernel.py`
- **Type :** python
- **Taille :** 22.1 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 464
- **Hash MD5 :** `0952215b72c0`
- **Références sortantes (10) :**
  - ❓ `import_module` → `__future__` *(l.22)*
  - ❓ `import_module` → `logging` *(l.23)*
  - ❓ `import_module` → `re` *(l.25)*
  - ❓ `import_module` → `dataclasses` *(l.26)*
  - ❓ `import_module` → `pathlib` *(l.27)*
  - ❓ `import_module` → `typing` *(l.28)*
  - ❓ `chemin_litteral` → `/home/agent/app/theories` *(l.62)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.80)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\validation_hol_unifiee.thy` *(l.142)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\geometrie_spectre_premier.thy` *(l.187)*

### `agent-multiloop-Gabriel-local\src\adapters\corpus\thy_analyzer.py`
- **Type :** python
- **Taille :** 8.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 193
- **Hash MD5 :** `d138c8e2add8`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.11)*
  - ❓ `import_module` → `re` *(l.12)*
  - ❓ `import_module` → `subprocess` *(l.14)*
  - ❓ `import_module` → `sys` *(l.15)*
  - ❓ `import_module` → `pathlib` *(l.16)*
  - ❓ `import_module` → `typing` *(l.17)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\scripts\isabelle_static_check.py` *(l.91)*

### `agent-multiloop-Gabriel-local\src\adapters\corpus\thy_loader.py`
- **Type :** python
- **Taille :** 3.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 92
- **Hash MD5 :** `776711566b0d`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.4)*
  - ❓ `import_module` → `os` *(l.5)*
  - ❓ `import_module` → `re` *(l.7)*
  - ❓ `import_module` → `pathlib` *(l.8)*
  - ❓ `import_module` → `typing` *(l.9)*
  - ❓ `chemin_litteral` → `/theories` *(l.22)*
  - ❓ `chemin_litteral` → `*.thy` *(l.30)*

### `agent-multiloop-Gabriel-local\src\adapters\gabriel_isabelle_bridge.py`
- **Type :** python
- **Taille :** 8.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 276
- **Hash MD5 :** `9b6aa2684646`
- **Références sortantes (9) :**
  - ❓ `import_module` → `asyncio` *(l.14)*
  - ❓ `import_module` → `json` *(l.16)*
  - ❓ `import_module` → `subprocess` *(l.17)*
  - ❓ `import_module` → `time` *(l.18)*
  - ❓ `import_module` → `pathlib` *(l.19)*
  - ❓ `import_module` → `typing` *(l.20)*
  - ❓ `import_module` → `logging` *(l.21)*
  - ❓ `chemin_litteral` → `/theories` *(l.29)*
  - ❓ `chemin_litteral` → `gabriel_{timestamp}.thy` *(l.53)*

### `agent-multiloop-Gabriel-local\src\adapters\gabriel_multiformat_manager.py`
- **Type :** python
- **Taille :** 11.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 331
- **Hash MD5 :** `6d8f3afd8848`
- **Références sortantes (9) :**
  - ❓ `import_module` → `pathlib` *(l.10)*
  - ❓ `import_module` → `subprocess` *(l.12)*
  - ❓ `import_module` → `json` *(l.13)*
  - ❓ `import_module` → `typing` *(l.14)*
  - ❓ `chemin_litteral` → `/home/agent/app/theories/projects` *(l.19)*
  - ❓ `chemin_litteral` → `projet_uni_car_savard_{i:02d}.thy` *(l.32)*
  - ❓ `chemin_litteral` → `projet_uni_car_savard_{i:02d}.txt` *(l.33)*
  - ❓ `chemin_litteral` → `projet_uni_car_savard_{project_num:02d}.thy` *(l.52)*
  - ❓ `chemin_litteral` → `projet_uni_car_savard_{project_num:02d}.txt` *(l.53)*

### `agent-multiloop-Gabriel-local\src\adapters\gabriel_project_manager.py`
- **Type :** python
- **Taille :** 8.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 253
- **Hash MD5 :** `a21a87539d61`
- **Références sortantes (8) :**
  - ❓ `import_module` → `pathlib` *(l.8)*
  - ❓ `import_module` → `subprocess` *(l.10)*
  - ❓ `import_module` → `time` *(l.11)*
  - ❓ `import_module` → `typing` *(l.12)*
  - ❓ `chemin_litteral` → `/home/agent/app/theories/projects` *(l.17)*
  - ❓ `chemin_litteral` → `projet_uni_car_savard_*.thy` *(l.24)*
  - ❓ `chemin_litteral` → `projet_uni_car_savard_{project_num:02d}.thy` *(l.44)*
  - ❓ `chemin_litteral` → `execution_projet_{template_num:02d}.thy` *(l.105)*

### `agent-multiloop-Gabriel-local\src\adapters\hol_integration.py`
- **Type :** python
- **Taille :** 3.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 118
- **Hash MD5 :** `615d6b650b17`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.6)*
  - ❓ `import_module` → `logging` *(l.7)*
  - ❓ `import_module` → `typing` *(l.9)*
  - ❓ `import_module` → `..spectral.hol_script_generator` *(l.10)*

### `agent-multiloop-Gabriel-local\src\adapters\hol_isabelle\__init__.py`
- **Type :** python
- **Taille :** 118.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 5
- **Hash MD5 :** `f618f4e13f61`
- **Références sortantes (1) :**
  - ❓ `import_module` → `.isabelle_adapter` *(l.2)*

### `agent-multiloop-Gabriel-local\src\adapters\hol_isabelle\isabelle_adapter.py`
- **Type :** python
- **Taille :** 5.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 154
- **Hash MD5 :** `bd30d57d105c`
- **Références sortantes (10) :**
  - ❓ `import_module` → `__future__` *(l.9)*
  - ❓ `import_module` → `logging` *(l.10)*
  - ❓ `import_module` → `os` *(l.12)*
  - ❓ `import_module` → `shutil` *(l.13)*
  - ❓ `import_module` → `subprocess` *(l.14)*
  - ❓ `import_module` → `pathlib` *(l.15)*
  - ❓ `import_module` → `typing` *(l.16)*
  - ❓ `chemin_litteral` → `/opt/Isabelle2025-2` *(l.28)*
  - ❓ `chemin_litteral` → `/theories` *(l.30)*
  - ❓ `chemin_litteral` → `{theory_name}.thy` *(l.115)*

### `agent-multiloop-Gabriel-local\src\adapters\llm\__init__.py`
- **Type :** python
- **Taille :** 157.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 6
- **Hash MD5 :** `1518d2f8acc1`
- **Références sortantes (2) :**
  - ❓ `import_module` → `.ollama_client` *(l.2)*
  - ❓ `import_module` → `.openai_client` *(l.3)*

### `agent-multiloop-Gabriel-local\src\adapters\llm\ollama_client.py`
- **Type :** python
- **Taille :** 4.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 124
- **Hash MD5 :** `e209382c1e4c`
- **Références sortantes (5) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `logging` *(l.3)*
  - ❓ `import_module` → `os` *(l.5)*
  - ❓ `import_module` → `httpx` *(l.6)*
  - ❓ `import_module` → `.utf8_sanitizer` *(l.8)*

### `agent-multiloop-Gabriel-local\src\adapters\llm\openai_client.py`
- **Type :** python
- **Taille :** 2.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 70
- **Hash MD5 :** `32b0d8dd13f5`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `logging` *(l.3)*
  - ❓ `import_module` → `os` *(l.5)*
  - ❓ `import_module` → `openai` *(l.6)*

### `agent-multiloop-Gabriel-local\src\adapters\llm\utf8_sanitizer.py`
- **Type :** python
- **Taille :** 3.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 89
- **Hash MD5 :** `b008163b944c`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.9)*
  - ❓ `import_module` → `logging` *(l.10)*
  - ❓ `import_module` → `unicodedata` *(l.12)*
  - ❓ `import_module` → `typing` *(l.13)*

### `agent-multiloop-Gabriel-local\src\adapters\wolfram\__init__.py`
- **Type :** python
- **Taille :** 341.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `9a061d4bdf47`
- **Références sortantes (1) :**
  - ❓ `import_module` → `.wolfram_client` *(l.2)*

### `agent-multiloop-Gabriel-local\src\adapters\wolfram\wolfram_client.py`
- **Type :** python
- **Taille :** 4.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 123
- **Hash MD5 :** `24398ea3e59a`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.8)*
  - ❓ `import_module` → `logging` *(l.9)*
  - ❓ `import_module` → `os` *(l.11)*
  - ❓ `import_module` → `typing` *(l.12)*
  - ❓ `import_module` → `httpx` *(l.13)*
  - ❓ `chemin_litteral` → `WOLFRAM_APP_ID absent ou non configure dans .env` *(l.63)*

### `agent-multiloop-Gabriel-local\src\advanced_analysis_criteria.py`
- **Type :** python
- **Taille :** 22.6 Ko
- **Modifié :** 2026-08-15 07:53:02
- **Lignes :** 601
- **Hash MD5 :** `9b38ec7b4c4e`
- **Références sortantes (8) :**
  - ❓ `import_module` → `__future__` *(l.19)*
  - ❓ `import_module` → `logging` *(l.21)*
  - ❓ `import_module` → `dataclasses` *(l.23)*
  - ❓ `import_module` → `pathlib` *(l.24)*
  - ❓ `import_module` → `typing` *(l.25)*
  - ❓ `import_module` → `enum` *(l.26)*
  - ❓ `import_module` → `re` *(l.27)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\src\complete_vision_system.py` *(l.409)*

### `agent-multiloop-Gabriel-local\src\advanced_vision_module.py`
- **Type :** python
- **Taille :** 25.1 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 742
- **Hash MD5 :** `92677ac47353`
- **Références sortantes (14) :**
  - ❓ `import_module` → `__future__` *(l.20)*
  - ❓ `import_module` → `logging` *(l.22)*
  - ❓ `import_module` → `dataclasses` *(l.24)*
  - ❓ `import_module` → `pathlib` *(l.25)*
  - ❓ `import_module` → `typing` *(l.26)*
  - ❓ `import_module` → `enum` *(l.27)*
  - ❓ `import_module` → `json` *(l.28)*
  - ❓ `import_module` → `math` *(l.29)*
  - ❓ `import_module` → `numpy` *(l.32)*
  - ❓ `import_module` → `PIL` *(l.38)*
  - ❓ `import_module` → `cv2` *(l.44)*
  - ❓ `import_module` → `pytesseract` *(l.50)*
  - ❓ `import_module` → `sys` *(l.726)*
  - ❓ `import_module` → `traceback` *(l.740)*

### `agent-multiloop-Gabriel-local\src\api\gabriel_http_api.py`
- **Type :** python
- **Taille :** 9.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 277
- **Hash MD5 :** `c5846567b70f`
- **Références sortantes (22) :**
  - ❓ `import_module` → `asyncio` *(l.12)*
  - ❓ `import_module` → `json` *(l.14)*
  - ❓ `import_module` → `logging` *(l.15)*
  - ❓ `import_module` → `datetime` *(l.16)*
  - ❓ `import_module` → `typing` *(l.17)*
  - ❓ `import_module` → `pathlib` *(l.18)*
  - ❓ `import_module` → `flask` *(l.19)*
  - ❓ `import_module` → `flask_cors` *(l.21)*
  - ❓ `import_module` → `werkzeug.utils` *(l.22)*
  - ❓ `Path()` → `/home/agent/app/data/isabelle-results` *(l.118)*
  - ❓ `Path()` → `/home/agent/app/data/universestaucarre-sync` *(l.199)*
  - ❓ `chemin_litteral` → `/api/*` *(l.31)*
  - ❓ `chemin_litteral` → `/query` *(l.32)*
  - ❓ `chemin_litteral` → `/isabelle/*` *(l.33)*
  - ❓ `chemin_litteral` → `/sync/*` *(l.34)*
  - ❓ `chemin_litteral` → `/isabelle/verify` *(l.95)*
  - ❓ `chemin_litteral` → `/theories/example.thy` *(l.100)*
  - ❓ `chemin_litteral` → `)}.json` *(l.121)*
  - ❓ `chemin_litteral` → `/health` *(l.145)*
  - ❓ `chemin_litteral` → `/sync/universestaucarre` *(l.159)*
  - ❓ `chemin_litteral` → `sync_{session_id}.json` *(l.202)*
  - ❓ `chemin_litteral` → `/stream` *(l.241)*

### `agent-multiloop-Gabriel-local\src\audit\__init__.py`
- **Type :** python
- **Taille :** 176.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 5
- **Hash MD5 :** `6a106f7308e2`
- **Références sortantes (1) :**
  - ❓ `import_module` → `.audit_store` *(l.2)*

### `agent-multiloop-Gabriel-local\src\audit\audit_store.py`
- **Type :** python
- **Taille :** 13.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 335
- **Hash MD5 :** `a073cac8da7c`
- **Références sortantes (15) :**
  - ❓ `import_module` → `__future__` *(l.4)*
  - ❓ `import_module` → `hashlib` *(l.5)*
  - ❓ `import_module` → `json` *(l.7)*
  - ❓ `import_module` → `logging` *(l.8)*
  - ❓ `import_module` → `re` *(l.9)*
  - ❓ `import_module` → `uuid` *(l.10)*
  - ❓ `import_module` → `dataclasses` *(l.11)*
  - ❓ `import_module` → `datetime` *(l.12)*
  - ❓ `import_module` → `pathlib` *(l.13)*
  - ❓ `import_module` → `typing` *(l.14)*
  - ❓ `import_module` → `..adapters.llm.utf8_sanitizer` *(l.15)*
  - ❓ `chemin_litteral` → `/home/agent/app/data/audits` *(l.107)*
  - ❓ `chemin_litteral` → `)}_{record.id}.json` *(l.175)*
  - ❓ `chemin_litteral` → `*_{record_id}.json` *(l.190)*
  - ❓ `chemin_litteral` → `*.json` *(l.213)*

### `agent-multiloop-Gabriel-local\src\cognitive\__init__.py`
- **Type :** python
- **Taille :** 1.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 33
- **Hash MD5 :** `ff43cfb51526`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.8)*
  - ❓ `import_module` → `.proof_trace` *(l.9)*
  - ❓ `import_module` → `.regime_ontology` *(l.11)*
  - ❓ `import_module` → `.epistemic` *(l.12)*
  - ❓ `import_module` → `.meta_reasoning` *(l.13)*
  - ❓ `import_module` → `.traced_calculations` *(l.14)*
  - ❓ `import_module` → `.engine_bridge` *(l.17)*

### `agent-multiloop-Gabriel-local\src\cognitive\engine_bridge.py`
- **Type :** python
- **Taille :** 8.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 235
- **Hash MD5 :** `7eb3082f5b1a`
- **Références sortantes (12) :**
  - ❓ `import_module` → `__future__` *(l.14)*
  - ❓ `import_module` → `dataclasses` *(l.15)*
  - ❓ `import_module` → `fractions` *(l.17)*
  - ❓ `import_module` → `pathlib` *(l.18)*
  - ❓ `import_module` → `typing` *(l.19)*
  - ❓ `import_module` → `.epistemic` *(l.20)*
  - ❓ `import_module` → `.meta_reasoning` *(l.22)*
  - ❓ `import_module` → `.proof_trace` *(l.23)*
  - ❓ `import_module` → `.regime_ontology` *(l.24)*
  - ❓ `import_module` → `.traced_calculations` *(l.25)*
  - ❓ `Path()` → `data/learning` *(l.34)*
  - ❓ `chemin_litteral` → `stats.json` *(l.44)*

### `agent-multiloop-Gabriel-local\src\cognitive\epistemic.py`
- **Type :** python
- **Taille :** 3.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 99
- **Hash MD5 :** `499aaccc4efd`
- **Références sortantes (5) :**
  - ❓ `import_module` → `__future__` *(l.10)*
  - ❓ `import_module` → `dataclasses` *(l.11)*
  - ❓ `import_module` → `datetime` *(l.13)*
  - ❓ `import_module` → `enum` *(l.14)*
  - ❓ `import_module` → `typing` *(l.15)*

### `agent-multiloop-Gabriel-local\src\cognitive\meta_reasoning.py`
- **Type :** python
- **Taille :** 5.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 146
- **Hash MD5 :** `f8125c9d7713`
- **Références sortantes (10) :**
  - ❓ `import_module` → `__future__` *(l.6)*
  - ❓ `import_module` → `json` *(l.7)*
  - ❓ `import_module` → `logging` *(l.9)*
  - ❓ `import_module` → `dataclasses` *(l.10)*
  - ❓ `import_module` → `datetime` *(l.11)*
  - ❓ `import_module` → `enum` *(l.12)*
  - ❓ `import_module` → `pathlib` *(l.13)*
  - ❓ `import_module` → `typing` *(l.14)*
  - ❓ `open_fichier` → `a` *(l.142)*
  - ❓ `chemin_litteral` → `data/learning/stats.json` *(l.64)*

### `agent-multiloop-Gabriel-local\src\cognitive\proof_trace.py`
- **Type :** python
- **Taille :** 3.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 96
- **Hash MD5 :** `2892e6b0bc20`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.6)*
  - ❓ `import_module` → `dataclasses` *(l.7)*
  - ❓ `import_module` → `datetime` *(l.9)*
  - ❓ `import_module` → `typing` *(l.10)*

### `agent-multiloop-Gabriel-local\src\cognitive\regime_ontology.py`
- **Type :** python
- **Taille :** 5.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 135
- **Hash MD5 :** `2e9474199045`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.11)*
  - ❓ `import_module` → `dataclasses` *(l.12)*
  - ❓ `import_module` → `enum` *(l.14)*
  - ❓ `import_module` → `typing` *(l.15)*

### `agent-multiloop-Gabriel-local\src\cognitive\traced_calculations.py`
- **Type :** python
- **Taille :** 8.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 280
- **Hash MD5 :** `784bb075737c`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.12)*
  - ❓ `import_module` → `json` *(l.13)*
  - ❓ `import_module` → `fractions` *(l.15)*
  - ❓ `import_module` → `typing` *(l.16)*
  - ❓ `import_module` → `.proof_trace` *(l.17)*
  - ❓ `import_module` → `..spectral.spectral_models` *(l.123)*

### `agent-multiloop-Gabriel-local\src\complete_validation_integration.py`
- **Type :** python
- **Taille :** 15.5 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 415
- **Hash MD5 :** `30250b968cdc`
- **Références sortantes (11) :**
  - ❓ `import_module` → `__future__` *(l.8)*
  - ❓ `import_module` → `logging` *(l.10)*
  - ❓ `import_module` → `dataclasses` *(l.12)*
  - ❓ `import_module` → `pathlib` *(l.13)*
  - ❓ `import_module` → `typing` *(l.14)*
  - ❓ `import_module` → `datetime` *(l.15)*
  - ❓ `import_module` → `json` *(l.16)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\src\complete_vision_system.py` *(l.19)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\src\parametric_validation_module.py` *(l.28)*
  - ❓ `import_module` → `time` *(l.107)*
  - ❓ `import_module` → `math` *(l.315)*

### `agent-multiloop-Gabriel-local\src\complete_vision_system.py`
- **Type :** python
- **Taille :** 16.2 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 408
- **Hash MD5 :** `13926cee5a62`
- **Références sortantes (11) :**
  - ❓ `import_module` → `__future__` *(l.18)*
  - ❓ `import_module` → `logging` *(l.20)*
  - ❓ `import_module` → `dataclasses` *(l.22)*
  - ❓ `import_module` → `pathlib` *(l.23)*
  - ❓ `import_module` → `typing` *(l.24)*
  - ❓ `import_module` → `datetime` *(l.25)*
  - ❓ `import_module` → `json` *(l.26)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\src\image_access_manager.py` *(l.29)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\src\vision_module.py` *(l.36)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\src\advanced_vision_module.py` *(l.42)*
  - ❓ `import_module` → `time` *(l.135)*

### `agent-multiloop-Gabriel-local\src\core\__init__.py`
- **Type :** python
- **Taille :** 25.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 2
- **Hash MD5 :** `dea6d7f665dc`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\src\core\config.py`
- **Type :** python
- **Taille :** 4.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 137
- **Hash MD5 :** `6b910b9d0d25`
- **Références sortantes (12) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `logging` *(l.3)*
  - ❓ `import_module` → `os` *(l.5)*
  - ❓ `import_module` → `pathlib` *(l.6)*
  - ❓ `import_module` → `typing` *(l.7)*
  - ❓ `import_module` → `yaml` *(l.8)*
  - ❓ `import_module` → `dotenv` *(l.10)*
  - ❓ `Path()` → `/home/agent/app/.env` *(l.30)*
  - ❓ `Path()` → `/home/agent/app/config.yaml` *(l.74)*
  - ❓ `chemin_litteral` → `env_file: - .env` *(l.59)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\config.yaml` *(l.72)*
  - ❓ `chemin_litteral` → `/theories` *(l.127)*

### `agent-multiloop-Gabriel-local\src\core\conversational_memory.py`
- **Type :** python
- **Taille :** 7.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 187
- **Hash MD5 :** `f5cb687537ad`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.18)*
  - ❓ `import_module` → `collections` *(l.19)*
  - ❓ `import_module` → `dataclasses` *(l.21)*
  - ❓ `import_module` → `typing` *(l.22)*

### `agent-multiloop-Gabriel-local\src\core\filesystem_access.py`
- **Type :** python
- **Taille :** 16.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 465
- **Hash MD5 :** `41aa4273ffa2`
- **Références sortantes (12) :**
  - ❓ `import_module` → `__future__` *(l.16)*
  - ❓ `import_module` → `base64` *(l.18)*
  - ❓ `import_module` → `mimetypes` *(l.20)*
  - ❓ `import_module` → `os` *(l.21)*
  - ❓ `import_module` → `dataclasses` *(l.22)*
  - ❓ `import_module` → `pathlib` *(l.23)*
  - ❓ `import_module` → `typing` *(l.24)*
  - ❓ `import_module` → `PIL` *(l.25)*
  - ❓ `import_module` → `anthropic` *(l.379)*
  - ❓ `chemin_litteral` → `/home/agent/app/theorie-savard` *(l.121)*
  - ❓ `chemin_litteral` → `/home/agent/app/data/theorie-savard` *(l.122)*
  - ❓ `chemin_litteral` → `/workspace/theorie-savard` *(l.123)*

### `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py`
- **Type :** python
- **Taille :** 4.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 107
- **Hash MD5 :** `a9ef74d3f34b`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.12)*
  - ❓ `import_module` → `logging` *(l.13)*
  - ❓ `import_module` → `sys` *(l.15)*
  - ❓ `import_module` → `pathlib` *(l.16)*
  - ❓ `import_module` → `typing` *(l.17)*
  - ❓ `import_module` → `memory.adaptateur_cognitif_rag` *(l.36)*
  - ❓ `import_module` → `memory.dictionnaire_spectral` *(l.37)*

### `agent-multiloop-Gabriel-local\src\core\latex_generator.py`
- **Type :** python
- **Taille :** 20.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 643
- **Hash MD5 :** `680c375515d5`
- **Références sortantes (8) :**
  - ❓ `import_module` → `re` *(l.19)*
  - ❓ `import_module` → `subprocess` *(l.21)*
  - ❓ `import_module` → `json` *(l.22)*
  - ❓ `import_module` → `pathlib` *(l.23)*
  - ❓ `import_module` → `typing` *(l.24)*
  - ❓ `import_module` → `dataclasses` *(l.25)*
  - ❓ `import_module` → `enum` *(l.26)*
  - ❓ `import_module` → `shutil` *(l.577)*

### `agent-multiloop-Gabriel-local\src\core\llm_manager.py`
- **Type :** python
- **Taille :** 15.3 Ko
- **Modifié :** 2026-08-15 14:49:32
- **Lignes :** 441
- **Hash MD5 :** `85c3d050b466`
- **Références sortantes (13) :**
  - ❓ `import_module` → `__future__` *(l.5)*
  - ❓ `import_module` → `logging` *(l.6)*
  - ❓ `import_module` → `os` *(l.8)*
  - ❓ `import_module` → `sys` *(l.9)*
  - ❓ `import_module` → `pathlib` *(l.10)*
  - ❓ `import_module` → `typing` *(l.11)*
  - ❓ `import_module` → `..adapters.llm.ollama_client` *(l.12)*
  - ❓ `import_module` → `..adapters.llm.openai_client` *(l.14)*
  - ❓ `import_module` → `..adapters.llm.utf8_sanitizer` *(l.15)*
  - ❓ `import_module` → `.conversational_memory` *(l.16)*
  - ❓ `import_module` → `anthropic` *(l.25)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` *(l.38)*
  - ❓ `import_module` → `secrets` *(l.71)*

### `agent-multiloop-Gabriel-local\src\core\logging_setup.py`
- **Type :** python
- **Taille :** 3.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 88
- **Hash MD5 :** `6c1aa3b78b15`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.11)*
  - ❓ `import_module` → `logging` *(l.12)*
  - ❓ `import_module` → `os` *(l.14)*
  - ❓ `import_module` → `sys` *(l.15)*
  - ❓ `import_module` → `pathlib` *(l.16)*
  - ❓ `chemin_litteral` → `./logs` *(l.26)*

### `agent-multiloop-Gabriel-local\src\core\orchestrator.py`
- **Type :** python
- **Taille :** 2.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 71
- **Hash MD5 :** `694d766d9b0f`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `logging` *(l.3)*
  - ❓ `import_module` → `typing` *(l.5)*
  - ❓ `import_module` → `.pipeline` *(l.6)*
  - ❓ `import_module` → `.pipeline_with_gap_detection` *(l.8)*
  - ❓ `import_module` → `.types` *(l.9)*

### `agent-multiloop-Gabriel-local\src\core\pipeline.py`
- **Type :** python
- **Taille :** 38.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 884
- **Hash MD5 :** `2f68030ad8f0`
- **Références sortantes (25) :**
  - ❓ `import_module` → `__future__` *(l.15)*
  - ❓ `import_module` → `logging` *(l.16)*
  - ❓ `import_module` → `uuid` *(l.18)*
  - ❓ `import_module` → `pathlib` *(l.19)*
  - ❓ `import_module` → `typing` *(l.20)*
  - ❓ `import_module` → `..adapters.corpus.thy_loader` *(l.21)*
  - ❓ `import_module` → `..adapters.hol_isabelle.isabelle_adapter` *(l.23)*
  - ❓ `import_module` → `..core.llm_manager` *(l.24)*
  - ❓ `import_module` → `..core.types` *(l.25)*
  - ❓ `import_module` → `..engines.abstraction` *(l.26)*
  - ❓ `import_module` → `..engines.concept_navigation` *(l.27)*
  - ❓ `import_module` → `..engines.generalization` *(l.28)*
  - ❓ `import_module` → `..engines.meta_reasoning` *(l.29)*
  - ❓ `import_module` → `..engines.numerical_verification` *(l.30)*
  - ❓ `import_module` → `..engines.theorem_discovery` *(l.31)*
  - ❓ `import_module` → `..multiloop` *(l.32)*
  - ❓ `import_module` → `..adapters.corpus.certainty_kernel` *(l.43)*
  - ❓ `import_module` → `..audit` *(l.44)*
  - ❓ `import_module` → `..cognitive` *(l.45)*
  - ❓ `import_module` → `..spectral` *(l.48)*
  - ❓ `import_module` → `.spectral_core` *(l.57)*
  - ❓ `import_module` → `..multiloop.llm_reformulator` *(l.117)*
  - ❓ `import_module` → `..multiloop.request_decomposer` *(l.794)*
  - ❓ `chemin_litteral` → `/theories` *(l.84)*
  - ❓ `chemin_litteral` → `/home/agent/app/data/audits` *(l.109)*

### `agent-multiloop-Gabriel-local\src\core\pipeline_with_gap_detection.py`
- **Type :** python
- **Taille :** 24.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 624
- **Hash MD5 :** `32629ffe949a`
- **Références sortantes (14) :**
  - ❓ `import_module` → `__future__` *(l.4)*
  - ❓ `import_module` → `logging` *(l.5)*
  - ❓ `import_module` → `re` *(l.7)*
  - ❓ `import_module` → `uuid` *(l.8)*
  - ❓ `import_module` → `typing` *(l.9)*
  - ❓ `import_module` → `..core.types` *(l.10)*
  - ❓ `import_module` → `..spectral.composite_absurdity_prover` *(l.12)*
  - ❓ `import_module` → `..spectral.gap_solver_corrected` *(l.16)*
  - ❓ `import_module` → `..spectral.prime_table` *(l.17)*
  - ❓ `import_module` → `..visualization` *(l.197)*
  - ❓ `import_module` → `..engines.question_graphs` *(l.198)*
  - ❓ `import_module` → `pathlib` *(l.246)*
  - ❓ `import_module` → `..audit` *(l.381)*
  - ❓ `Path()` → `data/graphs` *(l.251)*

### `agent-multiloop-Gabriel-local\src\core\plan_trifocal.py`
- **Type :** python
- **Taille :** 11.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 272
- **Hash MD5 :** `5416073a4c9b`
- **Références sortantes (8) :**
  - ❓ `import_module` → `dataclasses` *(l.16)*
  - ❓ `import_module` → `enum` *(l.18)*
  - ❓ `import_module` → `typing` *(l.19)*
  - ❓ `import_module` → `pathlib` *(l.20)*
  - ❓ `import_module` → `rich.panel` *(l.21)*
  - ❓ `import_module` → `rich.console` *(l.22)*
  - ❓ `import_module` → `rich.text` *(l.23)*
  - ❓ `import_module` → `rich.table` *(l.24)*

### `agent-multiloop-Gabriel-local\src\core\plan_trifocal_avec_image.py`
- **Type :** python
- **Taille :** 4.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 132
- **Hash MD5 :** `fe086ea9b52b`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.14)*
  - ❓ `import_module` → `os` *(l.16)*
  - ❓ `import_module` → `pathlib` *(l.18)*
  - ❓ `import_module` → `typing` *(l.19)*
  - ❓ `import_module` → `rich.console` *(l.20)*
  - ❓ `import_module` → `rich.panel` *(l.22)*
  - ❓ `import_module` → `.filesystem_access` *(l.23)*

### `agent-multiloop-Gabriel-local\src\core\planner.py`
- **Type :** python
- **Taille :** 1.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 33
- **Hash MD5 :** `bd83ad8e6dbc`
- **Références sortantes (2) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `typing` *(l.3)*

### `agent-multiloop-Gabriel-local\src\core\scientific_badge.py`
- **Type :** python
- **Taille :** 7.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 193
- **Hash MD5 :** `9e4f8a8f9dd4`
- **Références sortantes (6) :**
  - ❓ `import_module` → `enum` *(l.15)*
  - ❓ `import_module` → `dataclasses` *(l.17)*
  - ❓ `import_module` → `typing` *(l.18)*
  - ❓ `import_module` → `rich.text` *(l.19)*
  - ❓ `import_module` → `rich.panel` *(l.20)*
  - ❓ `import_module` → `rich.console` *(l.21)*

### `agent-multiloop-Gabriel-local\src\core\spectral_core.py`
- **Type :** python
- **Taille :** 37.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 885
- **Hash MD5 :** `6a4b830f4e9f`
- **Références sortantes (10) :**
  - ❓ `import_module` → `math` *(l.4)*
  - ❓ `import_module` → `dataclasses` *(l.5)*
  - ❓ `import_module` → `typing` *(l.6)*
  - ❓ `import_module` → `enum` *(l.7)*
  - ❓ `import_module` → `logging` *(l.8)*
  - ❓ `import_module` → `re` *(l.9)*
  - ❓ `import_module` → `..spectral.prime_table` *(l.46)*
  - ❓ `import_module` → `src.spectral.prime_table` *(l.52)*
  - ❓ `import_module` → `fractions` *(l.251)*
  - ❓ `import_module` → `..multiloop.forbidden_vocab` *(l.814)*

### `agent-multiloop-Gabriel-local\src\core\types.py`
- **Type :** python
- **Taille :** 2.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 93
- **Hash MD5 :** `f6ad7b103756`
- **Références sortantes (5) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `datetime` *(l.3)*
  - ❓ `import_module` → `enum` *(l.5)*
  - ❓ `import_module` → `typing` *(l.6)*
  - ❓ `import_module` → `pydantic` *(l.7)*

### `agent-multiloop-Gabriel-local\src\cost_manager.py`
- **Type :** python
- **Taille :** 6.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 164
- **Hash MD5 :** `95ea23c60446`
- **Références sortantes (4) :**
  - ❓ `import_module` → `logging` *(l.5)*
  - ❓ `import_module` → `os` *(l.7)*
  - ❓ `import_module` → `datetime` *(l.8)*
  - ❓ `import_module` → `typing` *(l.9)*

### `agent-multiloop-Gabriel-local\src\debug_toolkit\__init__.py`
- **Type :** python
- **Taille :** 724.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 20
- **Hash MD5 :** `bced7be93c7f`
- **Références sortantes (4) :**
  - ❓ `import_module` → `.registry` *(l.11)*
  - ❓ `import_module` → `.sympy_validator` *(l.12)*
  - ❓ `import_module` → `.mpmath_validator` *(l.13)*
  - ❓ `import_module` → `.z3_prover` *(l.14)*

### `agent-multiloop-Gabriel-local\src\debug_toolkit\mpmath_validator.py`
- **Type :** python
- **Taille :** 3.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 85
- **Hash MD5 :** `1514415dc974`
- **Références sortantes (3) :**
  - ❓ `import_module` → `__future__` *(l.8)*
  - ❓ `import_module` → `typing` *(l.9)*
  - ❓ `import_module` → `mpmath` *(l.11)*

### `agent-multiloop-Gabriel-local\src\debug_toolkit\registry.py`
- **Type :** python
- **Taille :** 2.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 72
- **Hash MD5 :** `0da10b87e000`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `importlib` *(l.3)*
  - ❓ `import_module` → `dataclasses` *(l.5)*
  - ❓ `import_module` → `typing` *(l.6)*

### `agent-multiloop-Gabriel-local\src\debug_toolkit\sympy_validator.py`
- **Type :** python
- **Taille :** 3.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `c6f1fec683cc`
- **Références sortantes (3) :**
  - ❓ `import_module` → `__future__` *(l.7)*
  - ❓ `import_module` → `typing` *(l.8)*
  - ❓ `import_module` → `sympy` *(l.10)*

### `agent-multiloop-Gabriel-local\src\debug_toolkit\z3_prover.py`
- **Type :** python
- **Taille :** 5.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 138
- **Hash MD5 :** `f4b4923a71bf`
- **Références sortantes (3) :**
  - ❓ `import_module` → `__future__` *(l.9)*
  - ❓ `import_module` → `typing` *(l.10)*
  - ❓ `import_module` → `z3` *(l.14)*

### `agent-multiloop-Gabriel-local\src\engines\__init__.py`
- **Type :** python
- **Taille :** 24.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 2
- **Hash MD5 :** `74008ad6604d`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\src\engines\abstraction\__init__.py`
- **Type :** python
- **Taille :** 157.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 5
- **Hash MD5 :** `ce8a0b536a17`
- **Références sortantes (1) :**
  - ❓ `import_module` → `.abstraction_layer` *(l.2)*

### `agent-multiloop-Gabriel-local\src\engines\abstraction\abstraction_layer.py`
- **Type :** python
- **Taille :** 12.1 Ko
- **Modifié :** 2026-08-15 14:51:02
- **Lignes :** 319
- **Hash MD5 :** `94d6778e763d`
- **Références sortantes (5) :**
  - ❓ `import_module` → `__future__` *(l.5)*
  - ❓ `import_module` → `logging` *(l.6)*
  - ❓ `import_module` → `re` *(l.8)*
  - ❓ `import_module` → `typing` *(l.9)*
  - ❓ `import_module` → `...core.types` *(l.10)*

### `agent-multiloop-Gabriel-local\src\engines\concept_navigation\__init__.py`
- **Type :** python
- **Taille :** 134.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 5
- **Hash MD5 :** `0d326e7d53bb`
- **Références sortantes (1) :**
  - ❓ `import_module` → `.navigator` *(l.2)*

### `agent-multiloop-Gabriel-local\src\engines\concept_navigation\navigator.py`
- **Type :** python
- **Taille :** 2.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 81
- **Hash MD5 :** `8d8f3fbf33f5`
- **Références sortantes (3) :**
  - ❓ `import_module` → `__future__` *(l.5)*
  - ❓ `import_module` → `typing` *(l.6)*
  - ❓ `import_module` → `networkx` *(l.8)*

### `agent-multiloop-Gabriel-local\src\engines\generalization\__init__.py`
- **Type :** python
- **Taille :** 140.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 5
- **Hash MD5 :** `1ca33a21cf04`
- **Références sortantes (1) :**
  - ❓ `import_module` → `.generalizer` *(l.2)*

### `agent-multiloop-Gabriel-local\src\engines\generalization\generalizer.py`
- **Type :** python
- **Taille :** 2.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 70
- **Hash MD5 :** `f3eeef7591ca`
- **Références sortantes (2) :**
  - ❓ `import_module` → `__future__` *(l.5)*
  - ❓ `import_module` → `typing` *(l.6)*

### `agent-multiloop-Gabriel-local\src\engines\geometrie_spectrale_engine.py`
- **Type :** python
- **Taille :** 12.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 324
- **Hash MD5 :** `9dd2c9789427`
- **Références sortantes (5) :**
  - ❓ `import_module` → `__future__` *(l.23)*
  - ❓ `import_module` → `logging` *(l.24)*
  - ❓ `import_module` → `dataclasses` *(l.26)*
  - ❓ `import_module` → `typing` *(l.27)*
  - ❓ `import_module` → `..spectral.spectral_models` *(l.28)*

### `agent-multiloop-Gabriel-local\src\engines\meta_reasoning\__init__.py`
- **Type :** python
- **Taille :** 179.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 5
- **Hash MD5 :** `63c958133b23`
- **Références sortantes (1) :**
  - ❓ `import_module` → `.meta_reasoning` *(l.2)*

### `agent-multiloop-Gabriel-local\src\engines\meta_reasoning\meta_reasoning.py`
- **Type :** python
- **Taille :** 6.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 142
- **Hash MD5 :** `9620d3a3ad5a`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.11)*
  - ❓ `import_module` → `logging` *(l.12)*
  - ❓ `import_module` → `typing` *(l.14)*
  - ❓ `import_module` → `...core.types` *(l.15)*

### `agent-multiloop-Gabriel-local\src\engines\numerical_verification\__init__.py`
- **Type :** python
- **Taille :** 133.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 5
- **Hash MD5 :** `4f3a4b1bd9f8`
- **Références sortantes (1) :**
  - ❓ `import_module` → `.numerical_verifier` *(l.2)*

### `agent-multiloop-Gabriel-local\src\engines\numerical_verification\numerical_verifier.py`
- **Type :** python
- **Taille :** 4.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 99
- **Hash MD5 :** `4f770cd4f3ce`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.12)*
  - ❓ `import_module` → `logging` *(l.13)*
  - ❓ `import_module` → `typing` *(l.15)*
  - ❓ `import_module` → `...adapters.wolfram` *(l.16)*

### `agent-multiloop-Gabriel-local\src\engines\question_graphs.py`
- **Type :** python
- **Taille :** 11.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 291
- **Hash MD5 :** `76ca75ed5853`
- **Références sortantes (13) :**
  - ❓ `import_module` → `src.engines.question_graphs` *(l.15)*
  - ❓ `import_module` → `__future__` *(l.20)*
  - ❓ `import_module` → `dataclasses` *(l.21)*
  - ❓ `import_module` → `datetime` *(l.23)*
  - ❓ `import_module` → `pathlib` *(l.24)*
  - ❓ `import_module` → `typing` *(l.25)*
  - ❓ `import_module` → `..core.spectral_core` *(l.26)*
  - ❓ `import_module` → `..spectral.rsp_curve` *(l.28)*
  - ❓ `import_module` → `..spectral.ratios` *(l.29)*
  - ❓ `import_module` → `..visualization.curves` *(l.30)*
  - ❓ `import_module` → `..visualization.png_renderer` *(l.33)*
  - ❓ `import_module` → `logging` *(l.244)*
  - ❓ `Path()` → `data/graphs` *(l.17)*

### `agent-multiloop-Gabriel-local\src\engines\theorem_discovery\__init__.py`
- **Type :** python
- **Taille :** 198.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 5
- **Hash MD5 :** `c08387a2a5cc`
- **Références sortantes (1) :**
  - ❓ `import_module` → `.discovery_loop` *(l.2)*

### `agent-multiloop-Gabriel-local\src\engines\theorem_discovery\discovery_loop.py`
- **Type :** python
- **Taille :** 1.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 50
- **Hash MD5 :** `adfe687c50be`
- **Références sortantes (2) :**
  - ❓ `import_module` → `__future__` *(l.5)*
  - ❓ `import_module` → `typing` *(l.6)*

### `agent-multiloop-Gabriel-local\src\gabriel_image_interface.py`
- **Type :** python
- **Taille :** 14.6 Ko
- **Modifié :** 2026-08-15 07:37:11
- **Lignes :** 413
- **Hash MD5 :** `f05734e31a6c`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.13)*
  - ❓ `import_module` → `logging` *(l.15)*
  - ❓ `import_module` → `pathlib` *(l.17)*
  - ❓ `import_module` → `typing` *(l.18)*
  - ❓ `import_module` → `re` *(l.19)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\src\complete_validation_integration.py` *(l.22)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\src\production_validation_system.py` *(l.28)*

### `agent-multiloop-Gabriel-local\src\gabriel_llm_integration_cache.py`
- **Type :** python
- **Taille :** 14.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 344
- **Hash MD5 :** `695e9b7f427d`
- **Références sortantes (6) :**
  - ❓ `import_module` → `logging` *(l.5)*
  - ❓ `import_module` → `typing` *(l.7)*
  - ❓ `import_module` → `src.llm_router` *(l.8)*
  - ❓ `import_module` → `src.prompt_injector` *(l.10)*
  - ❓ `import_module` → `src.cost_manager` *(l.11)*
  - ❓ `import_module` → `src.prompt_cache_manager` *(l.12)*

### `agent-multiloop-Gabriel-local\src\gabriel_llm_integration_safe.py`
- **Type :** python
- **Taille :** 8.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 207
- **Hash MD5 :** `e92eeefc50db`
- **Références sortantes (5) :**
  - ❓ `import_module` → `logging` *(l.5)*
  - ❓ `import_module` → `typing` *(l.7)*
  - ❓ `import_module` → `src.llm_router` *(l.8)*
  - ❓ `import_module` → `src.prompt_injector` *(l.10)*
  - ❓ `import_module` → `src.cost_manager` *(l.11)*

### `agent-multiloop-Gabriel-local\src\gabriel_llm_integration_v2.py`
- **Type :** python
- **Taille :** 10.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 260
- **Hash MD5 :** `255a4169ebf9`
- **Références sortantes (4) :**
  - ❓ `import_module` → `logging` *(l.5)*
  - ❓ `import_module` → `typing` *(l.7)*
  - ❓ `import_module` → `src.llm_router_v2` *(l.8)*
  - ❓ `import_module` → `memory.prompt_injector_enhanced` *(l.10)*

### `agent-multiloop-Gabriel-local\src\gabriel_vision_integration.py`
- **Type :** python
- **Taille :** 10.9 Ko
- **Modifié :** 2026-08-16 20:12:55
- **Lignes :** 305
- **Hash MD5 :** `1f54b0d2f53e`
- **Références sortantes (8) :**
  - ❓ `import_module` → `logging` *(l.18)*
  - ❓ `import_module` → `re` *(l.20)*
  - ❓ `import_module` → `pathlib` *(l.21)*
  - ❓ `import_module` → `typing` *(l.22)*
  - ❓ `import_module` → `enum` *(l.23)*
  - ❓ `import_module` → `PIL` *(l.171)*
  - ❓ `import_module` → `numpy` *(l.172)*
  - ❓ `chemin_litteral` → `/[^\s` *(l.89)*

### `agent-multiloop-Gabriel-local\src\hol4_gap_mixed_generator.py`
- **Type :** python
- **Taille :** 16.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 366
- **Hash MD5 :** `b51742c301a7`
- **Références sortantes (3) :**
  - ❓ `import_module` → `logging` *(l.5)*
  - ❓ `import_module` → `typing` *(l.7)*
  - ❓ `import_module` → `dataclasses` *(l.8)*

### `agent-multiloop-Gabriel-local\src\hol_isabelle_formal_generator.py`
- **Type :** python
- **Taille :** 21.0 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 681
- **Hash MD5 :** `adc82b4406e3`
- **Références sortantes (6) :**
  - ❓ `import_module` → `logging` *(l.5)*
  - ❓ `import_module` → `typing` *(l.7)*
  - ❓ `import_module` → `enum` *(l.8)*
  - ❓ `import_module` → `Mathlib.Data.Real.Basic` *(l.420)*
  - ❓ `import_module` → `Mathlib.Algebra.GroupPower.Basic` *(l.422)*
  - ❓ `import_module` → `Mathlib.Data.Complex.Basic` *(l.423)*

### `agent-multiloop-Gabriel-local\src\hol_lean_interface.py`
- **Type :** python
- **Taille :** 11.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 339
- **Hash MD5 :** `50dac1e112d3`
- **Références sortantes (11) :**
  - ❓ `import_module` → `os` *(l.5)*
  - ❓ `import_module` → `logging` *(l.7)*
  - ❓ `import_module` → `subprocess` *(l.8)*
  - ❓ `import_module` → `tempfile` *(l.9)*
  - ❓ `import_module` → `json` *(l.10)*
  - ❓ `import_module` → `typing` *(l.11)*
  - ❓ `import_module` → `dataclasses` *(l.12)*
  - ❓ `import_module` → `pathlib` *(l.13)*
  - ❓ `import_module` → `re` *(l.14)*
  - ❓ `chemin_litteral` → `/theories` *(l.34)*
  - ❓ `chemin_litteral` → `/lean` *(l.155)*

### `agent-multiloop-Gabriel-local\src\hol_proof_corrector.py`
- **Type :** python
- **Taille :** 11.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 301
- **Hash MD5 :** `526eaf28c1a5`
- **Références sortantes (5) :**
  - ❓ `import_module` → `logging` *(l.5)*
  - ❓ `import_module` → `typing` *(l.7)*
  - ❓ `import_module` → `dataclasses` *(l.8)*
  - ❓ `import_module` → `re` *(l.9)*
  - ❓ `import_module` → `src.isabelle_validator` *(l.10)*

### `agent-multiloop-Gabriel-local\src\image_access_manager.py`
- **Type :** python
- **Taille :** 19.8 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 547
- **Hash MD5 :** `4b3555786565`
- **Références sortantes (18) :**
  - ❓ `import_module` → `__future__` *(l.16)*
  - ❓ `import_module` → `logging` *(l.18)*
  - ❓ `import_module` → `hashlib` *(l.20)*
  - ❓ `import_module` → `shutil` *(l.21)*
  - ❓ `import_module` → `tempfile` *(l.22)*
  - ❓ `import_module` → `dataclasses` *(l.23)*
  - ❓ `import_module` → `pathlib` *(l.24)*
  - ❓ `import_module` → `typing` *(l.25)*
  - ❓ `import_module` → `enum` *(l.26)*
  - ❓ `import_module` → `datetime` *(l.27)*
  - ❓ `import_module` → `json` *(l.28)*
  - ❓ `import_module` → `re` *(l.29)*
  - ❓ `import_module` → `requests` *(l.32)*
  - ❓ `import_module` → `urllib.parse` *(l.39)*
  - ❓ `import_module` → `sys` *(l.508)*
  - ❓ `Path()` → `/tmp` *(l.85)*
  - ❓ `chemin_litteral` → `./images/graphique.jpg` *(l.487)*
  - ❓ `chemin_litteral` → `./images/figure.jpg` *(l.520)*

### `agent-multiloop-Gabriel-local\src\image_discovery_system.py`
- **Type :** python
- **Taille :** 15.8 Ko
- **Modifié :** 2026-08-15 07:48:05
- **Lignes :** 453
- **Hash MD5 :** `a1ce0e4476fd`
- **Références sortantes (23) :**
  - ❓ `import_module` → `__future__` *(l.18)*
  - ❓ `import_module` → `logging` *(l.20)*
  - ❓ `import_module` → `os` *(l.22)*
  - ❓ `import_module` → `time` *(l.23)*
  - ❓ `import_module` → `dataclasses` *(l.24)*
  - ❓ `import_module` → `pathlib` *(l.25)*
  - ❓ `import_module` → `typing` *(l.26)*
  - ❓ `import_module` → `datetime` *(l.27)*
  - ❓ `import_module` → `threading` *(l.28)*
  - ❓ `import_module` → `json` *(l.29)*
  - ❓ `import_module` → `difflib` *(l.32)*
  - ❓ `Path()` → `./data/image_index` *(l.57)*
  - ✅ `Path()` → `C:\Users` *(l.183)*
  - ❓ `Path()` → `/home` *(l.184)*
  - ✅ `Path()` → `agent-multiloop-Gabriel-local\src` *(l.185)*
  - ✅ `Path()` → `agent-multiloop-Gabriel-local` *(l.186)*
  - ✅ `Path()` → `agent-multiloop-Gabriel-local\data` *(l.191)*
  - ✅ `Path()` → `C:\theorie-mathematique` *(l.192)*
  - ❓ `Path()` → `C:/theories` *(l.193)*
  - ❓ `Path()` → `./figures` *(l.194)*
  - ❓ `Path()` → `./images` *(l.195)*
  - ❓ `Path()` → `./data` *(l.196)*
  - ❓ `chemin_litteral` → `image_index.json` *(l.61)*

### `agent-multiloop-Gabriel-local\src\isabelle_validator.py`
- **Type :** python
- **Taille :** 15.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 453
- **Hash MD5 :** `7327d05abdc1`
- **Références sortantes (14) :**
  - ❓ `import_module` → `subprocess` *(l.5)*
  - ❓ `import_module` → `os` *(l.7)*
  - ❓ `import_module` → `logging` *(l.8)*
  - ❓ `import_module` → `tempfile` *(l.9)*
  - ❓ `import_module` → `re` *(l.10)*
  - ❓ `import_module` → `typing` *(l.11)*
  - ❓ `import_module` → `dataclasses` *(l.12)*
  - ❓ `import_module` → `pathlib` *(l.13)*
  - ❓ `import_module` → `enum` *(l.14)*
  - ❓ `import_module` → `time` *(l.15)*
  - ❓ `chemin_litteral` → `/usr/bin/isabelle` *(l.77)*
  - ❓ `chemin_litteral` → `/opt/isabelle/bin/isabelle` *(l.78)*
  - ❓ `chemin_litteral` → `/Applications/Isabelle.app/Isabelle` *(l.80)*
  - ❓ `chemin_litteral` → `Exécute Isabelle sur fichier .thy` *(l.200)*

### `agent-multiloop-Gabriel-local\src\learning\debugging_expertise.py`
- **Type :** python
- **Taille :** 13.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 322
- **Hash MD5 :** `4507e07b5968`
- **Références sortantes (12) :**
  - ❓ `import_module` → `__future__` *(l.30)*
  - ❓ `import_module` → `hashlib` *(l.31)*
  - ❓ `import_module` → `json` *(l.33)*
  - ❓ `import_module` → `logging` *(l.34)*
  - ❓ `import_module` → `re` *(l.35)*
  - ❓ `import_module` → `dataclasses` *(l.36)*
  - ❓ `import_module` → `datetime` *(l.37)*
  - ❓ `import_module` → `pathlib` *(l.38)*
  - ❓ `import_module` → `typing` *(l.39)*
  - ❓ `Path()` → `/home/agent/app/data/expertise` *(l.159)*
  - ❓ `chemin_litteral` → `{record.session_id}.json` *(l.267)*
  - ❓ `chemin_litteral` → `*.json` *(l.274)*

### `agent-multiloop-Gabriel-local\src\learning\meta_learning_integration.py`
- **Type :** python
- **Taille :** 8.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 212
- **Hash MD5 :** `83fa790e75ba`
- **Références sortantes (9) :**
  - ❓ `import_module` → `__future__` *(l.16)*
  - ❓ `import_module` → `logging` *(l.17)*
  - ❓ `import_module` → `typing` *(l.19)*
  - ❓ `import_module` → `..core.types` *(l.20)*
  - ❓ `import_module` → `..learning.debugging_expertise` *(l.22)*
  - ❓ `import_module` → `..learning.slowmotion_recorder` *(l.23)*
  - ❓ `import_module` → `..multiloop.coherence_detector` *(l.24)*
  - ❓ `import_module` → `..multiloop.request_decomposer` *(l.25)*
  - ❓ `import_module` → `..multiloop.slow_motion_debugger` *(l.26)*

### `agent-multiloop-Gabriel-local\src\learning\slowmotion_recorder.py`
- **Type :** python
- **Taille :** 14.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 361
- **Hash MD5 :** `55563d4604dc`
- **Références sortantes (11) :**
  - ❓ `import_module` → `__future__` *(l.11)*
  - ❓ `import_module` → `logging` *(l.12)*
  - ❓ `import_module` → `re` *(l.14)*
  - ❓ `import_module` → `uuid` *(l.15)*
  - ❓ `import_module` → `typing` *(l.16)*
  - ❓ `import_module` → `..core.types` *(l.17)*
  - ❓ `import_module` → `..learning.debugging_expertise` *(l.19)*
  - ❓ `import_module` → `..multiloop.coherence_detector` *(l.27)*
  - ❓ `import_module` → `..multiloop.slow_motion_debugger` *(l.28)*
  - ❓ `import_module` → `..multiloop.request_decomposer` *(l.29)*
  - ❓ `import_module` → `datetime` *(l.350)*

### `agent-multiloop-Gabriel-local\src\llm_router.py`
- **Type :** python
- **Taille :** 16.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 418
- **Hash MD5 :** `007b6ffbbfe0`
- **Références sortantes (8) :**
  - ❓ `import_module` → `logging` *(l.5)*
  - ❓ `import_module` → `os` *(l.7)*
  - ❓ `import_module` → `typing` *(l.8)*
  - ❓ `import_module` → `dataclasses` *(l.9)*
  - ❓ `import_module` → `enum` *(l.10)*
  - ❓ `import_module` → `time` *(l.11)*
  - ❓ `import_module` → `anthropic` *(l.12)*
  - ❓ `import_module` → `openai` *(l.14)*

### `agent-multiloop-Gabriel-local\src\llm_router_cache_extension.py`
- **Type :** python
- **Taille :** 3.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 97
- **Hash MD5 :** `fc7d271f14b7`
- **Références sortantes (2) :**
  - ❓ `import_module` → `typing` *(l.5)*
  - ❓ `import_module` → `logging` *(l.7)*

### `agent-multiloop-Gabriel-local\src\llm_router_v2.py`
- **Type :** python
- **Taille :** 22.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 599
- **Hash MD5 :** `0f5c13c503a1`
- **Références sortantes (8) :**
  - ❓ `import_module` → `logging` *(l.8)*
  - ❓ `import_module` → `os` *(l.10)*
  - ❓ `import_module` → `typing` *(l.11)*
  - ❓ `import_module` → `dataclasses` *(l.12)*
  - ❓ `import_module` → `enum` *(l.13)*
  - ❓ `import_module` → `time` *(l.14)*
  - ❓ `import_module` → `anthropic` *(l.15)*
  - ❓ `import_module` → `openai` *(l.17)*

### `agent-multiloop-Gabriel-local\src\mathematical_engine.py`
- **Type :** python
- **Taille :** 11.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 343
- **Hash MD5 :** `096a4af618fe`
- **Références sortantes (15) :**
  - ❓ `import_module` → `os` *(l.5)*
  - ❓ `import_module` → `logging` *(l.7)*
  - ❓ `import_module` → `typing` *(l.8)*
  - ❓ `import_module` → `dataclasses` *(l.9)*
  - ❓ `import_module` → `pathlib` *(l.10)*
  - ❓ `import_module` → `json` *(l.11)*
  - ❓ `import_module` → `subprocess` *(l.12)*
  - ❓ `import_module` → `tempfile` *(l.13)*
  - ❓ `import_module` → `sympy` *(l.14)*
  - ❓ `import_module` → `sympy.ntheory` *(l.17)*
  - ❓ `import_module` → `mpmath` *(l.18)*
  - ❓ `chemin_litteral` → `Reference riemann_hypothesis_spectral.thy` *(l.141)*
  - ❓ `chemin_litteral` → `gap_distribution lemma in riemann_spectral.thy` *(l.181)*
  - ❓ `chemin_litteral` → `prime_decomposition in number_theory.thy` *(l.203)*
  - ❓ `chemin_litteral` → `prime_number_theorem in analytic_number_theory.thy` *(l.237)*

### `agent-multiloop-Gabriel-local\src\multiloop\__init__.py`
- **Type :** python
- **Taille :** 985.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 34
- **Hash MD5 :** `a05e17da285a`
- **Références sortantes (8) :**
  - ❓ `import_module` → `.critic` *(l.2)*
  - ❓ `import_module` → `.refinement_loop` *(l.3)*
  - ❓ `import_module` → `.silent_audit` *(l.4)*
  - ❓ `import_module` → `.coherence_detector` *(l.5)*
  - ❓ `import_module` → `.request_decomposer` *(l.6)*
  - ❓ `import_module` → `.slow_motion_debugger` *(l.7)*
  - ❓ `import_module` → `.verification_loop` *(l.8)*
  - ❓ `import_module` → `.pre_reasoner` *(l.11)*

### `agent-multiloop-Gabriel-local\src\multiloop\certainty_model.py`
- **Type :** python
- **Taille :** 18.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 449
- **Hash MD5 :** `bfe5e0b541b2`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.28)*
  - ❓ `import_module` → `dataclasses` *(l.29)*
  - ❓ `import_module` → `enum` *(l.31)*
  - ❓ `import_module` → `typing` *(l.32)*
  - ❓ `import_module` → `.request_decomposer` *(l.33)*
  - ❓ `import_module` → `..spectral.prime_table` *(l.405)*
  - ❓ `import_module` → `sympy` *(l.424)*

### `agent-multiloop-Gabriel-local\src\multiloop\coherence_detector.py`
- **Type :** python
- **Taille :** 5.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 124
- **Hash MD5 :** `d70652c2b83b`
- **Références sortantes (8) :**
  - ❓ `import_module` → `__future__` *(l.15)*
  - ❓ `import_module` → `re` *(l.16)*
  - ❓ `import_module` → `statistics` *(l.18)*
  - ❓ `import_module` → `dataclasses` *(l.19)*
  - ❓ `import_module` → `typing` *(l.20)*
  - ❓ `import_module` → `..core.spectral_core` *(l.21)*
  - ❓ `import_module` → `..core.types` *(l.23)*
  - ❓ `import_module` → `.forbidden_vocab` *(l.24)*

### `agent-multiloop-Gabriel-local\src\multiloop\critic.py`
- **Type :** python
- **Taille :** 5.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 119
- **Hash MD5 :** `c34de0aa52f3`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.10)*
  - ❓ `import_module` → `logging` *(l.11)*
  - ❓ `import_module` → `typing` *(l.13)*
  - ❓ `import_module` → `..core.llm_manager` *(l.14)*
  - ❓ `import_module` → `..core.types` *(l.16)*
  - ❓ `import_module` → `.forbidden_vocab` *(l.83)*
  - ❓ `import_module` → `re` *(l.109)*

### `agent-multiloop-Gabriel-local\src\multiloop\debat_orchestrator.py`
- **Type :** python
- **Taille :** 25.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 586
- **Hash MD5 :** `758e575da2f3`
- **Références sortantes (17) :**
  - ❓ `import_module` → `__future__` *(l.21)*
  - ❓ `import_module` → `asyncio` *(l.22)*
  - ❓ `import_module` → `datetime` *(l.24)*
  - ❓ `import_module` → `json` *(l.25)*
  - ❓ `import_module` → `logging` *(l.26)*
  - ❓ `import_module` → `os` *(l.27)*
  - ❓ `import_module` → `re` *(l.28)*
  - ❓ `import_module` → `unicodedata` *(l.29)*
  - ❓ `import_module` → `uuid` *(l.30)*
  - ❓ `import_module` → `dataclasses` *(l.31)*
  - ❓ `import_module` → `pathlib` *(l.32)*
  - ❓ `import_module` → `typing` *(l.33)*
  - ❓ `import_module` → `..core.llm_manager` *(l.34)*
  - ❓ `import_module` → `..spectral.spectral_knowledge` *(l.36)*
  - ❓ `Path()` → `data/debats` *(l.95)*
  - ❓ `chemin_litteral` → `{stem}.json` *(l.522)*
  - ❓ `chemin_litteral` → `{stem}.md` *(l.531)*

### `agent-multiloop-Gabriel-local\src\multiloop\domain_classifier.py`
- **Type :** python
- **Taille :** 12.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 300
- **Hash MD5 :** `cbfe60a973f3`
- **Références sortantes (4) :**
  - ❓ `import_module` → `re` *(l.26)*
  - ❓ `import_module` → `enum` *(l.28)*
  - ❓ `import_module` → `typing` *(l.29)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.64)*

### `agent-multiloop-Gabriel-local\src\multiloop\domain_gate.py`
- **Type :** python
- **Taille :** 8.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 256
- **Hash MD5 :** `0772b7d8e35e`
- **Références sortantes (5) :**
  - ❓ `import_module` → `logging` *(l.13)*
  - ❓ `import_module` → `typing` *(l.15)*
  - ❓ `import_module` → `dataclasses` *(l.16)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\src\multiloop\domain_classifier.py` *(l.17)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\src\multiloop\gabriel_domain_config.py` *(l.25)*

### `agent-multiloop-Gabriel-local\src\multiloop\forbidden_vocab.py`
- **Type :** python
- **Taille :** 4.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 107
- **Hash MD5 :** `5c2670ae3f53`
- **Références sortantes (2) :**
  - ❓ `import_module` → `__future__` *(l.23)*
  - ❓ `import_module` → `re` *(l.24)*

### `agent-multiloop-Gabriel-local\src\multiloop\gabriel_domain_config.py`
- **Type :** python
- **Taille :** 10.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 275
- **Hash MD5 :** `78c8ac49944d`
- **Références sortantes (6) :**
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.41)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\geometrie_spectre_premier.thy` *(l.42)*
  - ❓ `chemin_litteral` → `chaos_harmonic_discrete.thy` *(l.49)*
  - ❓ `chemin_litteral` → `univers_carre_postulat.thy` *(l.54)*
  - ❓ `chemin_litteral` → `espace_philippot.thy` *(l.59)*
  - ❓ `chemin_litteral` → `Requête technique HOL/Isabelle sur methode_spectral.thy` *(l.69)*

### `agent-multiloop-Gabriel-local\src\multiloop\llm_reformulator.py`
- **Type :** python
- **Taille :** 13.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 346
- **Hash MD5 :** `1ce831ea784e`
- **Références sortantes (10) :**
  - ❓ `import_module` → `__future__` *(l.29)*
  - ❓ `import_module` → `asyncio` *(l.30)*
  - ❓ `import_module` → `logging` *(l.32)*
  - ❓ `import_module` → `re` *(l.33)*
  - ❓ `import_module` → `dataclasses` *(l.34)*
  - ❓ `import_module` → `typing` *(l.35)*
  - ❓ `import_module` → `..core.llm_manager` *(l.36)*
  - ❓ `import_module` → `.request_decomposer` *(l.38)*
  - ❓ `import_module` → `time` *(l.172)*
  - ❓ `import_module` → `.forbidden_vocab` *(l.302)*

### `agent-multiloop-Gabriel-local\src\multiloop\logical_loop.py`
- **Type :** python
- **Taille :** 12.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 325
- **Hash MD5 :** `3301b2017eef`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.24)*
  - ❓ `import_module` → `dataclasses` *(l.25)*
  - ❓ `import_module` → `typing` *(l.27)*
  - ❓ `import_module` → `.certainty_model` *(l.28)*
  - ❓ `import_module` → `.request_decomposer` *(l.30)*
  - ❓ `import_module` → `..spectral.prime_table` *(l.279)*
  - ❓ `import_module` → `sympy` *(l.291)*

### `agent-multiloop-Gabriel-local\src\multiloop\pre_reasoner.py`
- **Type :** python
- **Taille :** 18.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 424
- **Hash MD5 :** `f13739c48121`
- **Références sortantes (12) :**
  - ❓ `import_module` → `__future__` *(l.38)*
  - ❓ `import_module` → `re` *(l.39)*
  - ❓ `import_module` → `logging` *(l.41)*
  - ❓ `import_module` → `dataclasses` *(l.42)*
  - ❓ `import_module` → `enum` *(l.43)*
  - ❓ `import_module` → `typing` *(l.44)*
  - ❓ `chemin_litteral` → `/rapide` *(l.391)*
  - ❓ `chemin_litteral` → `/standard` *(l.392)*
  - ❓ `chemin_litteral` → `/approfondi` *(l.393)*
  - ❓ `chemin_litteral` → `/complet` *(l.394)*
  - ❓ `chemin_litteral` → `/tres_complexe` *(l.395)*
  - ❓ `chemin_litteral` → `/instantane` *(l.396)*

### `agent-multiloop-Gabriel-local\src\multiloop\refinement_loop.py`
- **Type :** python
- **Taille :** 6.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 169
- **Hash MD5 :** `1df0189808e5`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.9)*
  - ❓ `import_module` → `logging` *(l.10)*
  - ❓ `import_module` → `typing` *(l.12)*
  - ❓ `import_module` → `..core.llm_manager` *(l.13)*
  - ❓ `import_module` → `..core.types` *(l.15)*
  - ❓ `import_module` → `..spectral.spectral_knowledge` *(l.16)*
  - ❓ `import_module` → `.critic` *(l.17)*

### `agent-multiloop-Gabriel-local\src\multiloop\refinement_loop_fixed.py`
- **Type :** python
- **Taille :** 5.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 144
- **Hash MD5 :** `c290b9374ad1`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.11)*
  - ❓ `import_module` → `logging` *(l.12)*
  - ❓ `import_module` → `typing` *(l.14)*
  - ❓ `import_module` → `..core.llm_manager` *(l.15)*
  - ❓ `import_module` → `..core.types` *(l.17)*
  - ❓ `import_module` → `..spectral.spectral_knowledge` *(l.18)*
  - ❓ `import_module` → `.critic` *(l.19)*

### `agent-multiloop-Gabriel-local\src\multiloop\request_decomposer.py`
- **Type :** python
- **Taille :** 18.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 425
- **Hash MD5 :** `0865e2590209`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.10)*
  - ❓ `import_module` → `re` *(l.11)*
  - ❓ `import_module` → `dataclasses` *(l.13)*
  - ❓ `import_module` → `typing` *(l.14)*

### `agent-multiloop-Gabriel-local\src\multiloop\request_decomposer_patch.py`
- **Type :** python
- **Taille :** 5.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 154
- **Hash MD5 :** `84bf0de9656b`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.10)*
  - ❓ `import_module` → `re` *(l.11)*
  - ❓ `import_module` → `logging` *(l.13)*
  - ❓ `import_module` → `typing` *(l.14)*

### `agent-multiloop-Gabriel-local\src\multiloop\silent_audit.py`
- **Type :** python
- **Taille :** 6.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 171
- **Hash MD5 :** `bb3de7aed7ff`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.12)*
  - ❓ `import_module` → `logging` *(l.13)*
  - ❓ `import_module` → `typing` *(l.15)*
  - ❓ `import_module` → `..core.llm_manager` *(l.16)*
  - ❓ `import_module` → `..core.spectral_core` *(l.18)*
  - ❓ `import_module` → `..core.types` *(l.19)*
  - ❓ `import_module` → `..spectral.spectral_knowledge` *(l.20)*

### `agent-multiloop-Gabriel-local\src\multiloop\slow_motion_debugger.py`
- **Type :** python
- **Taille :** 34.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 793
- **Hash MD5 :** `1aea60c06f69`
- **Références sortantes (16) :**
  - ❓ `import_module` → `__future__` *(l.23)*
  - ❓ `import_module` → `logging` *(l.24)*
  - ❓ `import_module` → `dataclasses` *(l.26)*
  - ❓ `import_module` → `datetime` *(l.27)*
  - ❓ `import_module` → `typing` *(l.28)*
  - ❓ `import_module` → `..adapters.corpus.certainty_kernel` *(l.29)*
  - ❓ `import_module` → `..audit` *(l.31)*
  - ❓ `import_module` → `..core.spectral_core` *(l.32)*
  - ❓ `import_module` → `..core.types` *(l.33)*
  - ❓ `import_module` → `..spectral.prime_table` *(l.34)*
  - ❓ `import_module` → `.certainty_model` *(l.35)*
  - ❓ `import_module` → `.coherence_detector` *(l.36)*
  - ❓ `import_module` → `.logical_loop` *(l.37)*
  - ❓ `import_module` → `.request_decomposer` *(l.38)*
  - ❓ `import_module` → `.llm_reformulator` *(l.247)*
  - ❓ `import_module` → `sympy` *(l.493)*

### `agent-multiloop-Gabriel-local\src\multiloop\slowmotion_trigger.py`
- **Type :** python
- **Taille :** 6.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 165
- **Hash MD5 :** `89bc3164599f`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.18)*
  - ❓ `import_module` → `logging` *(l.19)*
  - ❓ `import_module` → `re` *(l.21)*
  - ❓ `import_module` → `typing` *(l.22)*
  - ❓ `import_module` → `..core.types` *(l.23)*
  - ❓ `import_module` → `..multiloop.coherence_detector` *(l.25)*
  - ❓ `import_module` → `..multiloop.slow_motion_debugger` *(l.26)*

### `agent-multiloop-Gabriel-local\src\multiloop\verification_loop.py`
- **Type :** python
- **Taille :** 16.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 397
- **Hash MD5 :** `eac960c50c9d`
- **Références sortantes (12) :**
  - ❓ `import_module` → `__future__` *(l.18)*
  - ❓ `import_module` → `asyncio` *(l.19)*
  - ❓ `import_module` → `logging` *(l.21)*
  - ❓ `import_module` → `re` *(l.22)*
  - ❓ `import_module` → `dataclasses` *(l.23)*
  - ❓ `import_module` → `pathlib` *(l.24)*
  - ❓ `import_module` → `typing` *(l.25)*
  - ❓ `import_module` → `..adapters.hol_isabelle.isabelle_adapter` *(l.26)*
  - ❓ `import_module` → `..adapters.wolfram.wolfram_client` *(l.28)*
  - ❓ `import_module` → `..audit` *(l.31)*
  - ❓ `import_module` → `..core.spectral_core` *(l.32)*
  - ❓ `import_module` → `..spectral.prime_table` *(l.33)*

### `agent-multiloop-Gabriel-local\src\parametric_validation_module.py`
- **Type :** python
- **Taille :** 34.0 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 944
- **Hash MD5 :** `27e9c125a3f3`
- **Références sortantes (12) :**
  - ❓ `import_module` → `__future__` *(l.17)*
  - ❓ `import_module` → `logging` *(l.19)*
  - ❓ `import_module` → `math` *(l.21)*
  - ❓ `import_module` → `dataclasses` *(l.22)*
  - ❓ `import_module` → `pathlib` *(l.23)*
  - ❓ `import_module` → `typing` *(l.24)*
  - ❓ `import_module` → `enum` *(l.25)*
  - ❓ `import_module` → `json` *(l.26)*
  - ❓ `import_module` → `re` *(l.27)*
  - ❓ `import_module` → `numpy` *(l.30)*
  - ❓ `import_module` → `PIL` *(l.36)*
  - ❓ `import_module` → `cv2` *(l.42)*

### `agent-multiloop-Gabriel-local\src\pdf_rag_processor.py`
- **Type :** python
- **Taille :** 13.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 373
- **Hash MD5 :** `fe6a7fa5c264`
- **Références sortantes (13) :**
  - ❓ `import_module` → `os` *(l.5)*
  - ❓ `import_module` → `logging` *(l.7)*
  - ❓ `import_module` → `typing` *(l.8)*
  - ❓ `import_module` → `pathlib` *(l.9)*
  - ❓ `import_module` → `json` *(l.10)*
  - ❓ `import_module` → `re` *(l.11)*
  - ❓ `import_module` → `dataclasses` *(l.12)*
  - ❓ `import_module` → `datetime` *(l.13)*
  - ❓ `import_module` → `PyPDF2` *(l.16)*
  - ❓ `import_module` → `numpy` *(l.23)*
  - ❓ `chemin_litteral` → `/Title` *(l.74)*
  - ❓ `chemin_litteral` → `/Author` *(l.75)*
  - ❓ `chemin_litteral` → `/CreationDate` *(l.76)*

### `agent-multiloop-Gabriel-local\src\production_validation_system.py`
- **Type :** python
- **Taille :** 30.8 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 801
- **Hash MD5 :** `6fc813a51afc`
- **Références sortantes (13) :**
  - ❓ `import_module` → `__future__` *(l.14)*
  - ❓ `import_module` → `logging` *(l.16)*
  - ❓ `import_module` → `dataclasses` *(l.18)*
  - ❓ `import_module` → `pathlib` *(l.19)*
  - ❓ `import_module` → `typing` *(l.20)*
  - ❓ `import_module` → `enum` *(l.21)*
  - ❓ `import_module` → `datetime` *(l.22)*
  - ❓ `import_module` → `json` *(l.23)*
  - ❓ `import_module` → `math` *(l.24)*
  - ❓ `import_module` → `statistics` *(l.25)*
  - ❓ `import_module` → `numpy` *(l.28)*
  - ❓ `import_module` → `scipy` *(l.34)*
  - ❓ `import_module` → `cv2` *(l.40)*

### `agent-multiloop-Gabriel-local\src\prompt_cache_manager.py`
- **Type :** python
- **Taille :** 12.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 364
- **Hash MD5 :** `1c017842ce66`
- **Références sortantes (5) :**
  - ❓ `import_module` → `logging` *(l.5)*
  - ❓ `import_module` → `hashlib` *(l.7)*
  - ❓ `import_module` → `typing` *(l.8)*
  - ❓ `import_module` → `dataclasses` *(l.9)*
  - ❓ `import_module` → `datetime` *(l.10)*

### `agent-multiloop-Gabriel-local\src\prompt_injector.py`
- **Type :** python
- **Taille :** 663.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 24
- **Hash MD5 :** `e46e796f3274`
- **Références sortantes (2) :**
  - ❓ `import_module` → `__future__` *(l.7)*
  - ❓ `import_module` → `memory.prompt_injector_enhanced` *(l.8)*

### `agent-multiloop-Gabriel-local\src\spectral\__init__.py`
- **Type :** python
- **Taille :** 2.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 46
- **Hash MD5 :** `07412100e7ef`
- **Références sortantes (7) :**
  - ❓ `import_module` → `.suites` *(l.2)*
  - ❓ `import_module` → `.digamma` *(l.7)*
  - ❓ `import_module` → `.ratios` *(l.8)*
  - ❓ `import_module` → `.gaps` *(l.12)*
  - ❓ `import_module` → `.reconstructor` *(l.16)*
  - ❓ `import_module` → `.prime_table` *(l.17)*
  - ❓ `import_module` → `.plan_trifocal` *(l.18)*

### `agent-multiloop-Gabriel-local\src\spectral\_primes_data.py`
- **Type :** python
- **Taille :** 6.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 105
- **Hash MD5 :** `009076704ee8`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\src\spectral\composite_absurdity_prover.py`
- **Type :** python
- **Taille :** 8.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 253
- **Hash MD5 :** `9bdab0b4dd91`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.22)*
  - ❓ `import_module` → `dataclasses` *(l.23)*
  - ❓ `import_module` → `typing` *(l.25)*
  - ❓ `import_module` → `.prime_table` *(l.26)*

### `agent-multiloop-Gabriel-local\src\spectral\digamma.py`
- **Type :** python
- **Taille :** 3.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 92
- **Hash MD5 :** `c1ed0c89fc0d`
- **Références sortantes (3) :**
  - ❓ `import_module` → `__future__` *(l.14)*
  - ❓ `import_module` → `fractions` *(l.15)*
  - ❓ `import_module` → `.suites` *(l.17)*

### `agent-multiloop-Gabriel-local\src\spectral\digamma_pure.py`
- **Type :** python
- **Taille :** 7.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 206
- **Hash MD5 :** `0681cd7498a6`
- **Références sortantes (5) :**
  - ❓ `import_module` → `__future__` *(l.28)*
  - ❓ `import_module` → `decimal` *(l.29)*
  - ❓ `import_module` → `fractions` *(l.31)*
  - ❓ `import_module` → `math` *(l.32)*
  - ❓ `import_module` → `typing` *(l.33)*

### `agent-multiloop-Gabriel-local\src\spectral\gap_cognitive_model.py`
- **Type :** python
- **Taille :** 11.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 276
- **Hash MD5 :** `e09341e38a20`
- **Références sortantes (5) :**
  - ❓ `import_module` → `__future__` *(l.23)*
  - ❓ `import_module` → `logging` *(l.24)*
  - ❓ `import_module` → `dataclasses` *(l.26)*
  - ❓ `import_module` → `typing` *(l.27)*
  - ❓ `import_module` → `re` *(l.230)*

### `agent-multiloop-Gabriel-local\src\spectral\gap_compute.py`
- **Type :** python
- **Taille :** 6.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 179
- **Hash MD5 :** `a1b3907a1a9e`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.24)*
  - ❓ `import_module` → `dataclasses` *(l.25)*
  - ❓ `import_module` → `fractions` *(l.27)*
  - ❓ `import_module` → `typing` *(l.28)*
  - ❓ `import_module` → `..core.spectral_core` *(l.29)*
  - ❓ `import_module` → `..spectral.prime_table` *(l.31)*

### `agent-multiloop-Gabriel-local\src\spectral\gap_solver_corrected.py`
- **Type :** python
- **Taille :** 11.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 317
- **Hash MD5 :** `43ea536d177a`
- **Références sortantes (5) :**
  - ❓ `import_module` → `__future__` *(l.21)*
  - ❓ `import_module` → `logging` *(l.22)*
  - ❓ `import_module` → `dataclasses` *(l.24)*
  - ❓ `import_module` → `typing` *(l.25)*
  - ❓ `import_module` → `.prime_table` *(l.26)*

### `agent-multiloop-Gabriel-local\src\spectral\gap_validation.py`
- **Type :** python
- **Taille :** 7.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 229
- **Hash MD5 :** `89384adf393c`
- **Références sortantes (3) :**
  - ❓ `import_module` → `fractions` *(l.6)*
  - ❓ `import_module` → `math` *(l.7)*
  - ❓ `import_module` → `src.spectral.prime_table` *(l.183)*

### `agent-multiloop-Gabriel-local\src\spectral\gaps.py`
- **Type :** python
- **Taille :** 5.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 167
- **Hash MD5 :** `701b5ddbca2c`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.15)*
  - ❓ `import_module` → `fractions` *(l.16)*
  - ❓ `import_module` → `.suites` *(l.18)*
  - ❓ `import_module` → `..core.types` *(l.20)*

### `agent-multiloop-Gabriel-local\src\spectral\hol_script_generator.py`
- **Type :** python
- **Taille :** 8.5 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 253
- **Hash MD5 :** `abc07314a249`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.6)*
  - ❓ `import_module` → `logging` *(l.7)*
  - ❓ `import_module` → `typing` *(l.9)*
  - ❓ `import_module` → `fractions` *(l.152)*

### `agent-multiloop-Gabriel-local\src\spectral\plan_trifocal.py`
- **Type :** python
- **Taille :** 14.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 325
- **Hash MD5 :** `77f863a4bac4`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.25)*
  - ❓ `import_module` → `dataclasses` *(l.26)*
  - ❓ `import_module` → `enum` *(l.28)*
  - ❓ `import_module` → `fractions` *(l.29)*
  - ❓ `import_module` → `typing` *(l.30)*
  - ❓ `import_module` → `.spectral_models` *(l.193)*
  - ❓ `import_module` → `..cognitive` *(l.284)*

### `agent-multiloop-Gabriel-local\src\spectral\prime_table.py`
- **Type :** python
- **Taille :** 984.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 38
- **Hash MD5 :** `6847ecab6206`
- **Références sortantes (2) :**
  - ❓ `import_module` → `__future__` *(l.8)*
  - ❓ `import_module` → `._primes_data` *(l.9)*

### `agent-multiloop-Gabriel-local\src\spectral\psi_savard.py`
- **Type :** python
- **Taille :** 9.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 259
- **Hash MD5 :** `ebbf4d8129fd`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.25)*
  - ❓ `import_module` → `math` *(l.26)*
  - ❓ `import_module` → `typing` *(l.28)*
  - ❓ `import_module` → `.suites` *(l.29)*

### `agent-multiloop-Gabriel-local\src\spectral\ratios.py`
- **Type :** python
- **Taille :** 9.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 255
- **Hash MD5 :** `ecc43c3e8845`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.11)*
  - ❓ `import_module` → `fractions` *(l.12)*
  - ❓ `import_module` → `.suites` *(l.14)*
  - ❓ `import_module` → `..core.types` *(l.16)*

### `agent-multiloop-Gabriel-local\src\spectral\reconstructor.py`
- **Type :** python
- **Taille :** 4.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 122
- **Hash MD5 :** `16f210b53816`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.10)*
  - ❓ `import_module` → `fractions` *(l.11)*
  - ❓ `import_module` → `.digamma` *(l.13)*
  - ❓ `import_module` → `.suites` *(l.15)*

### `agent-multiloop-Gabriel-local\src\spectral\rsp_command.py`
- **Type :** python
- **Taille :** 3.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 90
- **Hash MD5 :** `7277e615b7ea`
- **Références sortantes (5) :**
  - ❓ `import_module` → `__future__` *(l.15)*
  - ❓ `import_module` → `random` *(l.16)*
  - ❓ `import_module` → `re` *(l.18)*
  - ❓ `import_module` → `typing` *(l.19)*
  - ❓ `import_module` → `..core.spectral_core` *(l.20)*

### `agent-multiloop-Gabriel-local\src\spectral\rsp_curve.py`
- **Type :** python
- **Taille :** 7.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 209
- **Hash MD5 :** `9e4559c152b4`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.14)*
  - ❓ `import_module` → `typing` *(l.15)*
  - ❓ `import_module` → `..core.spectral_core` *(l.17)*
  - ❓ `import_module` → `.ratios` *(l.19)*

### `agent-multiloop-Gabriel-local\src\spectral\spectral_knowledge.py`
- **Type :** python
- **Taille :** 14.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 283
- **Hash MD5 :** `5eb2522de167`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.12)*

### `agent-multiloop-Gabriel-local\src\spectral\spectral_models.py`
- **Type :** python
- **Taille :** 12.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 348
- **Hash MD5 :** `8b8e1875f4c3`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.16)*
  - ❓ `import_module` → `abc` *(l.17)*
  - ❓ `import_module` → `dataclasses` *(l.19)*
  - ❓ `import_module` → `fractions` *(l.20)*
  - ❓ `import_module` → `typing` *(l.21)*
  - ❓ `chemin_litteral` → `/ (sum_B(A_pos) - sum_B(B_pos))` *(l.175)*

### `agent-multiloop-Gabriel-local\src\spectral\suites.py`
- **Type :** python
- **Taille :** 3.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 109
- **Hash MD5 :** `19988f7cb08c`
- **Références sortantes (2) :**
  - ❓ `import_module` → `__future__` *(l.5)*
  - ❓ `import_module` → `fractions` *(l.6)*

### `agent-multiloop-Gabriel-local\src\spectral\tchebychev_savard_pipeline.py`
- **Type :** python
- **Taille :** 7.4 Ko
- **Modifié :** 2026-08-15 19:34:13
- **Lignes :** 217
- **Hash MD5 :** `51ec11921f7b`
- **Références sortantes (3) :**
  - ❓ `import_module` → `math` *(l.12)*
  - ❓ `import_module` → `typing` *(l.14)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\src\spectral\prime_table.py` *(l.15)*

### `agent-multiloop-Gabriel-local\src\ui\__init__.py`
- **Type :** python
- **Taille :** 100.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 5
- **Hash MD5 :** `9b06f72fd2f4`
- **Références sortantes (1) :**
  - ❓ `import_module` → `.cli` *(l.2)*

### `agent-multiloop-Gabriel-local\src\ui\ask_gabriel.py`
- **Type :** python
- **Taille :** 18.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 362
- **Hash MD5 :** `1e150ca9cb55`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.10)*
  - ❓ `import_module` → `dataclasses` *(l.11)*
  - ❓ `import_module` → `typing` *(l.13)*
  - ❓ `chemin_litteral` → `    - methode_spectral.thy` *(l.189)*
  - ❓ `chemin_litteral` → `    - geometrie_spectre_premier.thy` *(l.190)*
  - ❓ `chemin_litteral` → `    - riemann_spectral.thy` *(l.191)*
  - ❓ `chemin_litteral` → `     -> Verifiez que les valeurs attendues correspondent a .thy` *(l.295)*

### `agent-multiloop-Gabriel-local\src\ui\ci_status.py`
- **Type :** python
- **Taille :** 6.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 187
- **Hash MD5 :** `4de324d7f4df`
- **Références sortantes (10) :**
  - ❓ `import_module` → `__future__` *(l.9)*
  - ❓ `import_module` → `os` *(l.10)*
  - ❓ `import_module` → `re` *(l.12)*
  - ❓ `import_module` → `subprocess` *(l.13)*
  - ❓ `import_module` → `sys` *(l.14)*
  - ❓ `import_module` → `dataclasses` *(l.15)*
  - ❓ `import_module` → `pathlib` *(l.16)*
  - ❓ `chemin_litteral` → `/app/tests` *(l.76)*
  - ❓ `chemin_litteral` → `/home/agent/app/tests` *(l.76)*
  - ❓ `chemin_litteral` → `/workspace/tests` *(l.76)*

### `agent-multiloop-Gabriel-local\src\ui\cinematic_display.py`
- **Type :** python
- **Taille :** 11.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 310
- **Hash MD5 :** `6fc5d5e1c86c`
- **Références sortantes (9) :**
  - ❓ `import_module` → `__future__` *(l.12)*
  - ❓ `import_module` → `time` *(l.13)*
  - ❓ `import_module` → `dataclasses` *(l.15)*
  - ❓ `import_module` → `enum` *(l.16)*
  - ❓ `import_module` → `typing` *(l.17)*
  - ❓ `import_module` → `rich.console` *(l.119)*
  - ❓ `import_module` → `rich.panel` *(l.262)*
  - ❓ `import_module` → `rich.text` *(l.263)*
  - ❓ `import_module` → `rich.box` *(l.264)*

### `agent-multiloop-Gabriel-local\src\ui\cinematic_orchestrator.py`
- **Type :** python
- **Taille :** 6.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 186
- **Hash MD5 :** `e935e9526a92`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.15)*
  - ❓ `import_module` → `logging` *(l.16)*
  - ❓ `import_module` → `typing` *(l.18)*
  - ❓ `import_module` → `.complexity_analyzer` *(l.19)*
  - ❓ `import_module` → `.cinematic_display` *(l.21)*
  - ❓ `import_module` → `re` *(l.178)*

### `agent-multiloop-Gabriel-local\src\ui\cli.py`
- **Type :** python
- **Taille :** 164.9 Ko
- **Modifié :** 2026-08-04 14:34:22
- **Lignes :** 3565
- **Hash MD5 :** `d657d2e355eb`
- **Références sortantes (51) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `asyncio` *(l.3)*
  - ❓ `import_module` → `logging` *(l.5)*
  - ❓ `import_module` → `os` *(l.6)*
  - ❓ `import_module` → `time` *(l.7)*
  - ❓ `import_module` → `pathlib` *(l.8)*
  - ❓ `import_module` → `typing` *(l.9)*
  - ❓ `import_module` → `rich.align` *(l.10)*
  - ❓ `import_module` → `rich.console` *(l.12)*
  - ❓ `import_module` → `rich.live` *(l.13)*
  - ❓ `import_module` → `rich.panel` *(l.14)*
  - ❓ `import_module` → `rich.rule` *(l.15)*
  - ❓ `import_module` → `rich.spinner` *(l.16)*
  - ❓ `import_module` → `rich.table` *(l.17)*
  - ❓ `import_module` → `rich.text` *(l.18)*
  - ❓ `import_module` → `..core.config` *(l.19)*
  - ❓ `import_module` → `..core.orchestrator` *(l.21)*
  - ❓ `import_module` → `..core.types` *(l.22)*
  - ❓ `import_module` → `.ci_status` *(l.23)*
  - ❓ `import_module` → `.debug_session` *(l.24)*
  - ❓ `import_module` → `.keybindings` *(l.25)*
  - ❓ `import_module` → `datetime` *(l.107)*
  - ❓ `import_module` → `random` *(l.108)*
  - ❓ `import_module` → `src.cognitive` *(l.334)*
  - ❓ `import_module` → `..core.plan_trifocal_avec_image` *(l.416)*
  - ❓ `import_module` → `..spectral` *(l.459)*
  - ❓ `import_module` → `..spectral.psi_savard` *(l.485)*
  - ❓ `import_module` → `..spectral.digamma_pure` *(l.580)*
  - ❓ `import_module` → `..adapters.corpus.thy_analyzer` *(l.611)*
  - ❓ `import_module` → `re` *(l.685)*
  - ❓ `import_module` → `..spectral.gap_compute` *(l.760)*
  - ❓ `import_module` → `src.audit` *(l.770)*
  - ❓ `import_module` → `src.spectral.rsp_curve` *(l.831)*
  - ❓ `import_module` → `src.spectral.rsp_command` *(l.866)*
  - ❓ `import_module` → `src.core.spectral_core` *(l.867)*
  - ❓ `import_module` → `json` *(l.1156)*
  - ❓ `import_module` → `.ask_gabriel` *(l.1381)*
  - ❓ `import_module` → `src.engines.geometrie_spectrale_engine` *(l.1451)*
  - ❓ `import_module` → `src.engines.question_graphs` *(l.1539)*
  - ❓ `import_module` → `..multiloop.debat_orchestrator` *(l.1648)*
  - ❓ `import_module` → `src.spectral` *(l.1795)*
  - ❓ `import_module` → `..core.filesystem_access` *(l.1976)*
  - ❓ `import_module` → `src.core.config` *(l.2087)*
  - ❓ `import_module` → `anthropic` *(l.2233)*
  - ❓ `import_module` → `src.visualization` *(l.2619)*
  - ❓ `import_module` → `..multiloop.pre_reasoner` *(l.3467)*
  - ❓ `Path()` → `theories/projects` *(l.627)*
  - ❓ `Path()` → `data/graphs` *(l.1611)*
  - ❓ `Path()` → `/app/agent-multiloop-Gabriel-local` *(l.2091)*
  - ❓ `Path()` → `/app` *(l.2092)*
  - ❓ `chemin_litteral` → `1000 premiers indexes  -  Sections I a XII de methode_spectral.thy` *(l.213)*

### `agent-multiloop-Gabriel-local\src\ui\complexity_analyzer.py`
- **Type :** python
- **Taille :** 10.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 308
- **Hash MD5 :** `2316aac6cb78`
- **Références sortantes (5) :**
  - ❓ `import_module` → `__future__` *(l.15)*
  - ❓ `import_module` → `re` *(l.16)*
  - ❓ `import_module` → `dataclasses` *(l.18)*
  - ❓ `import_module` → `enum` *(l.19)*
  - ❓ `import_module` → `typing` *(l.20)*

### `agent-multiloop-Gabriel-local\src\ui\debug_session.py`
- **Type :** python
- **Taille :** 23.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 559
- **Hash MD5 :** `4660dba5b138`
- **Références sortantes (16) :**
  - ❓ `import_module` → `__future__` *(l.24)*
  - ❓ `import_module` → `string` *(l.25)*
  - ❓ `import_module` → `dataclasses` *(l.27)*
  - ❓ `import_module` → `typing` *(l.28)*
  - ❓ `import_module` → `rich.console` *(l.29)*
  - ❓ `import_module` → `rich.panel` *(l.31)*
  - ❓ `import_module` → `rich.table` *(l.32)*
  - ❓ `import_module` → `..adapters.corpus.certainty_kernel` *(l.33)*
  - ❓ `import_module` → `..audit` *(l.35)*
  - ❓ `import_module` → `..core.spectral_core` *(l.36)*
  - ❓ `import_module` → `..core.types` *(l.37)*
  - ❓ `import_module` → `..debug_toolkit` *(l.38)*
  - ❓ `import_module` → `..multiloop.coherence_detector` *(l.41)*
  - ❓ `import_module` → `..multiloop.request_decomposer` *(l.42)*
  - ❓ `import_module` → `..multiloop.slow_motion_debugger` *(l.45)*
  - ❓ `import_module` → `..spectral.prime_table` *(l.331)*

### `agent-multiloop-Gabriel-local\src\ui\keybindings.py`
- **Type :** python
- **Taille :** 6.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 171
- **Hash MD5 :** `0f9d84db5d98`
- **Références sortantes (5) :**
  - ❓ `import_module` → `__future__` *(l.17)*
  - ❓ `import_module` → `logging` *(l.18)*
  - ❓ `import_module` → `pathlib` *(l.20)*
  - ❓ `import_module` → `typing` *(l.21)*
  - ❓ `import_module` → `readline` *(l.27)*

### `agent-multiloop-Gabriel-local\src\ui\latex_commands.py`
- **Type :** python
- **Taille :** 9.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 308
- **Hash MD5 :** `94b235626ce8`
- **Références sortantes (7) :**
  - ❓ `import_module` → `pathlib` *(l.16)*
  - ❓ `import_module` → `typing` *(l.18)*
  - ❓ `import_module` → `rich.console` *(l.19)*
  - ❓ `import_module` → `rich.panel` *(l.20)*
  - ❓ `import_module` → `rich.table` *(l.21)*
  - ❓ `import_module` → `rich.text` *(l.22)*
  - ❓ `import_module` → `.latex_generator` *(l.23)*

### `agent-multiloop-Gabriel-local\src\validation_hol_knowledge.py`
- **Type :** python
- **Taille :** 14.6 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 417
- **Hash MD5 :** `b90c6a658bed`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.7)*
  - ❓ `import_module` → `logging` *(l.9)*
  - ❓ `import_module` → `dataclasses` *(l.11)*
  - ❓ `import_module` → `pathlib` *(l.12)*
  - ❓ `import_module` → `typing` *(l.13)*
  - ❓ `import_module` → `json` *(l.14)*
  - ❓ `chemin_litteral` → `Représente un théorème du fichier validation_hol_unifiee.thy` *(l.21)*

### `agent-multiloop-Gabriel-local\src\vision_module.py`
- **Type :** python
- **Taille :** 22.5 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 697
- **Hash MD5 :** `b7d381ea69e4`
- **Références sortantes (14) :**
  - ❓ `import_module` → `__future__` *(l.19)*
  - ❓ `import_module` → `logging` *(l.21)*
  - ❓ `import_module` → `dataclasses` *(l.23)*
  - ❓ `import_module` → `pathlib` *(l.24)*
  - ❓ `import_module` → `typing` *(l.25)*
  - ❓ `import_module` → `enum` *(l.26)*
  - ❓ `import_module` → `json` *(l.27)*
  - ❓ `import_module` → `re` *(l.28)*
  - ❓ `import_module` → `numpy` *(l.31)*
  - ❓ `import_module` → `PIL` *(l.38)*
  - ❓ `import_module` → `cv2` *(l.45)*
  - ❓ `import_module` → `matplotlib.pyplot` *(l.464)*
  - ❓ `import_module` → `sys` *(l.659)*
  - ❓ `import_module` → `traceback` *(l.695)*

### `agent-multiloop-Gabriel-local\src\visualization\__init__.py`
- **Type :** python
- **Taille :** 1.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 44
- **Hash MD5 :** `cadd5dec794f`
- **Références sortantes (8) :**
  - ❓ `import_module` → `src.visualization` *(l.10)*
  - ❓ `import_module` → `__future__` *(l.17)*
  - ❓ `import_module` → `.curves` *(l.18)*
  - ❓ `import_module` → `.ascii_renderer` *(l.26)*
  - ❓ `import_module` → `.rich_renderer` *(l.27)*
  - ❓ `import_module` → `.png_renderer` *(l.28)*
  - ❓ `import_module` → `.auto_trigger` *(l.29)*
  - ❓ `Path()` → `data/graphs` *(l.15)*

### `agent-multiloop-Gabriel-local\src\visualization\ascii_renderer.py`
- **Type :** python
- **Taille :** 3.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 112
- **Hash MD5 :** `e4eb1ea77905`
- **Références sortantes (3) :**
  - ❓ `import_module` → `__future__` *(l.6)*
  - ❓ `import_module` → `math` *(l.7)*
  - ❓ `import_module` → `.curves` *(l.9)*

### `agent-multiloop-Gabriel-local\src\visualization\auto_trigger.py`
- **Type :** python
- **Taille :** 20.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 511
- **Hash MD5 :** `afb42b2e8760`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.12)*
  - ❓ `import_module` → `re` *(l.13)*
  - ❓ `import_module` → `unicodedata` *(l.15)*
  - ❓ `import_module` → `dataclasses` *(l.16)*
  - ❓ `import_module` → `typing` *(l.17)*
  - ❓ `import_module` → `.curves` *(l.18)*

### `agent-multiloop-Gabriel-local\src\visualization\curves.py`
- **Type :** python
- **Taille :** 24.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 531
- **Hash MD5 :** `ad0ac9523bdb`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.9)*
  - ❓ `import_module` → `dataclasses` *(l.10)*
  - ❓ `import_module` → `datetime` *(l.12)*
  - ❓ `import_module` → `enum` *(l.13)*
  - ❓ `import_module` → `math` *(l.14)*
  - ❓ `import_module` → `typing` *(l.15)*
  - ❓ `import_module` → `..core.spectral_core` *(l.16)*

### `agent-multiloop-Gabriel-local\src\visualization\png_renderer.py`
- **Type :** python
- **Taille :** 14.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 356
- **Hash MD5 :** `c21b553ac135`
- **Références sortantes (8) :**
  - ❓ `import_module` → `__future__` *(l.12)*
  - ❓ `import_module` → `datetime` *(l.13)*
  - ❓ `import_module` → `pathlib` *(l.15)*
  - ❓ `import_module` → `typing` *(l.16)*
  - ❓ `import_module` → `.curves` *(l.17)*
  - ❓ `import_module` → `matplotlib` *(l.21)*
  - ❓ `import_module` → `matplotlib.pyplot` *(l.23)*
  - ❓ `import_module` → `textwrap` *(l.351)*

### `agent-multiloop-Gabriel-local\src\visualization\rich_renderer.py`
- **Type :** python
- **Taille :** 2.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 91
- **Hash MD5 :** `d3294b65c46d`
- **Références sortantes (3) :**
  - ❓ `import_module` → `__future__` *(l.6)*
  - ❓ `import_module` → `rich.table` *(l.7)*
  - ❓ `import_module` → `.curves` *(l.9)*

### `agent-multiloop-Gabriel-local\start-agent.ps1`
- **Type :** autre
- **Taille :** 7.1 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 177
- **Hash MD5 :** `d543555e2857`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\test-integration.sh`
- **Type :** shell
- **Taille :** 4.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 154
- **Hash MD5 :** `c35327475bf1`
- **Références sortantes (2) :**
  - ❓ `shell_appel` → `Connect` *(l.151)*
  - ❓ `shell_appel` → `See` *(l.152)*

### `agent-multiloop-Gabriel-local\test_rsa_capability.py`
- **Type :** python
- **Taille :** 6.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 168
- **Hash MD5 :** `3a6e195282af`
- **Références sortantes (2) :**
  - ❓ `import_module` → `src.spectral_ratio_analyzer` *(l.10)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\gabriel_mathematical.py` *(l.93)*

### `agent-multiloop-Gabriel-local\test_spectral_gabriel.py`
- **Type :** python
- **Taille :** 5.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 173
- **Hash MD5 :** `707a52a53abb`
- **Références sortantes (5) :**
  - ❓ `import_module` → `sys` *(l.12)*
  - ❓ `import_module` → `logging` *(l.14)*
  - ❓ `import_module` → `pathlib` *(l.15)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\src\core\spectral_core.py` *(l.26)*
  - ❓ `import_module` → `traceback` *(l.166)*

### `agent-multiloop-Gabriel-local\tests\.gitkeep`
- **Type :** autre
- **Taille :** 0.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 1
- **Hash MD5 :** `d41d8cd98f00`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\tests\conftest.py`
- **Type :** python
- **Taille :** 182.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 8
- **Hash MD5 :** `c55e5015c50a`
- **Références sortantes (2) :**
  - ❓ `import_module` → `sys` *(l.2)*
  - ❓ `import_module` → `pathlib` *(l.3)*

### `agent-multiloop-Gabriel-local\tests\test_adaptive_scale_v336.py`
- **Type :** python
- **Taille :** 6.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 143
- **Hash MD5 :** `b7dee4e7e42d`
- **Références sortantes (8) :**
  - ❓ `import_module` → `__future__` *(l.11)*
  - ❓ `import_module` → `pytest` *(l.12)*
  - ❓ `import_module` → `pathlib` *(l.14)*
  - ❓ `import_module` → `src.core.spectral_core` *(l.15)*
  - ❓ `import_module` → `src.engines.question_graphs` *(l.17)*
  - ❓ `import_module` → `src.visualization.curves` *(l.18)*
  - ❓ `import_module` → `src.visualization.png_renderer` *(l.19)*
  - ❓ `import_module` → `src.visualization.auto_trigger` *(l.128)*

### `agent-multiloop-Gabriel-local\tests\test_ask_gabriel.py`
- **Type :** python
- **Taille :** 3.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 124
- **Hash MD5 :** `d0a6c97fad94`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `pytest` *(l.3)*
  - ❓ `import_module` → `src.ui.ask_gabriel` *(l.5)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.106)*

### `agent-multiloop-Gabriel-local\tests\test_audit_store.py`
- **Type :** python
- **Taille :** 12.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 339
- **Hash MD5 :** `3a6121ea22a5`
- **Références sortantes (16) :**
  - ❓ `import_module` → `__future__` *(l.5)*
  - ❓ `import_module` → `json` *(l.6)*
  - ❓ `import_module` → `sys` *(l.8)*
  - ❓ `import_module` → `tempfile` *(l.9)*
  - ❓ `import_module` → `pathlib` *(l.10)*
  - ❓ `import_module` → `unittest.mock` *(l.11)*
  - ❓ `import_module` → `pytest` *(l.12)*
  - ❓ `import_module` → `rich.console` *(l.17)*
  - ❓ `import_module` → `src.adapters.corpus.certainty_kernel` *(l.19)*
  - ❓ `import_module` → `src.audit` *(l.21)*
  - ❓ `import_module` → `src.core.spectral_core` *(l.22)*
  - ❓ `import_module` → `src.core.types` *(l.23)*
  - ❓ `import_module` → `src.multiloop.coherence_detector` *(l.24)*
  - ❓ `import_module` → `src.multiloop.slow_motion_debugger` *(l.25)*
  - ❓ `import_module` → `src.ui.debug_session` *(l.26)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.194)*

### `agent-multiloop-Gabriel-local\tests\test_auto_graphs_nl_and_chaos_savard_trigger.py`
- **Type :** python
- **Taille :** 8.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 218
- **Hash MD5 :** `e560a49b6b07`
- **Références sortantes (10) :**
  - ❓ `import_module` → `__future__` *(l.5)*
  - ❓ `import_module` → `pathlib` *(l.6)*
  - ❓ `import_module` → `pytest` *(l.8)*
  - ❓ `import_module` → `src.core.spectral_core` *(l.9)*
  - ❓ `import_module` → `src.visualization.auto_trigger` *(l.11)*
  - ❓ `import_module` → `src.visualization.curves` *(l.12)*
  - ❓ `import_module` → `src.core.pipeline_with_gap_detection` *(l.147)*
  - ❓ `import_module` → `src.core.types` *(l.148)*
  - ❓ `import_module` → `inspect` *(l.182)*
  - ❓ `import_module` → `src.engines.question_graphs` *(l.199)*

### `agent-multiloop-Gabriel-local\tests\test_auto_trigger.py`
- **Type :** python
- **Taille :** 7.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 185
- **Hash MD5 :** `5fe111ebf832`
- **Références sortantes (3) :**
  - ❓ `import_module` → `__future__` *(l.6)*
  - ❓ `import_module` → `pytest` *(l.7)*
  - ❓ `import_module` → `src.visualization` *(l.9)*

### `agent-multiloop-Gabriel-local\tests\test_auto_trigger_conversational_context.py`
- **Type :** python
- **Taille :** 5.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 132
- **Hash MD5 :** `22bee941b4da`
- **Références sortantes (3) :**
  - ❓ `import_module` → `__future__` *(l.14)*
  - ❓ `import_module` → `pytest` *(l.15)*
  - ❓ `import_module` → `src.visualization.auto_trigger` *(l.17)*

### `agent-multiloop-Gabriel-local\tests\test_auto_trigger_opinion_context_v330.py`
- **Type :** python
- **Taille :** 4.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 102
- **Hash MD5 :** `8d3f7f3f86df`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.11)*
  - ❓ `import_module` → `pytest` *(l.12)*
  - ❓ `import_module` → `src.visualization.auto_trigger` *(l.14)*
  - ❓ `import_module` → `src.visualization.curves` *(l.16)*

### `agent-multiloop-Gabriel-local\tests\test_banque_qr_sentinelle.py`
- **Type :** python
- **Taille :** 7.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 207
- **Hash MD5 :** `a56339480df6`
- **Références sortantes (10) :**
  - ❓ `import_module` → `__future__` *(l.7)*
  - ❓ `import_module` → `sys` *(l.8)*
  - ❓ `import_module` → `pathlib` *(l.10)*
  - ❓ `import_module` → `pytest` *(l.11)*
  - ❓ `import_module` → `re` *(l.71)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\memory\banque_qr_methode_spectrale.md` *(l.17)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.191)*
  - ❓ `chemin_litteral` → `espace_philippot.thy` *(l.195)*
  - ❓ `chemin_litteral` → `mecanique_discret.thy` *(l.196)*
  - ❓ `chemin_litteral` → `postulat_carre.thy` *(l.197)*

### `agent-multiloop-Gabriel-local\tests\test_bloc_chaotique_ordonne_v330.py`
- **Type :** python
- **Taille :** 5.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 143
- **Hash MD5 :** `e9681de81889`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.8)*
  - ❓ `import_module` → `pytest` *(l.9)*
  - ❓ `import_module` → `src.multiloop.request_decomposer` *(l.11)*
  - ❓ `import_module` → `src.core.spectral_core` *(l.13)*

### `agent-multiloop-Gabriel-local\tests\test_blocs_v343.py`
- **Type :** python
- **Taille :** 10.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 250
- **Hash MD5 :** `c80b111603ee`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `re` *(l.3)*
  - ❓ `import_module` → `unicodedata` *(l.5)*
  - ❓ `import_module` → `pathlib` *(l.6)*
  - ❓ `import_module` → `pytest` *(l.7)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.12)*

### `agent-multiloop-Gabriel-local\tests\test_cartouche_uniforme_ascii.py`
- **Type :** python
- **Taille :** 7.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 203
- **Hash MD5 :** `5a36fcd38917`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.18)*
  - ❓ `import_module` → `sys` *(l.19)*
  - ❓ `import_module` → `pathlib` *(l.21)*
  - ❓ `import_module` → `pytest` *(l.22)*
  - ❓ `import_module` → `re` *(l.74)*
  - ❓ `Path()` → `/app/agent-multiloop-Gabriel-local` *(l.180)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.6)*

### `agent-multiloop-Gabriel-local\tests\test_certainty_model_and_logical_loop.py`
- **Type :** python
- **Taille :** 10.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 233
- **Hash MD5 :** `725caa413e83`
- **Références sortantes (12) :**
  - ❓ `import_module` → `__future__` *(l.8)*
  - ❓ `import_module` → `src.multiloop.certainty_model` *(l.9)*
  - ❓ `import_module` → `src.multiloop.logical_loop` *(l.13)*
  - ❓ `import_module` → `src.multiloop.request_decomposer` *(l.14)*
  - ❓ `import_module` → `src.multiloop.slow_motion_debugger` *(l.15)*
  - ❓ `import_module` → `src.multiloop.coherence_detector` *(l.16)*
  - ❓ `import_module` → `src.core.spectral_core` *(l.17)*
  - ❓ `import_module` → `src.adapters.corpus.certainty_kernel` *(l.18)*
  - ❓ `import_module` → `src.core.types` *(l.19)*
  - ❓ `import_module` → `collections` *(l.43)*
  - ❓ `import_module` → `src.spectral.prime_table` *(l.117)*
  - ❓ `import_module` → `json` *(l.140)*

### `agent-multiloop-Gabriel-local\tests\test_chaos_savard_and_question_graphs.py`
- **Type :** python
- **Taille :** 11.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 302
- **Hash MD5 :** `eafe8a4bd3d4`
- **Références sortantes (10) :**
  - ❓ `import_module` → `__future__` *(l.11)*
  - ❓ `import_module` → `fractions` *(l.12)*
  - ❓ `import_module` → `pathlib` *(l.14)*
  - ❓ `import_module` → `pytest` *(l.15)*
  - ❓ `import_module` → `src.core.spectral_core` *(l.17)*
  - ❓ `import_module` → `src.spectral.ratios` *(l.19)*
  - ❓ `import_module` → `src.spectral.rsp_curve` *(l.24)*
  - ❓ `import_module` → `src.engines.question_graphs` *(l.167)*
  - ❓ `import_module` → `src.ui.cli` *(l.292)*
  - ❓ `import_module` → `inspect` *(l.297)*

### `agent-multiloop-Gabriel-local\tests\test_ci_regex_and_env_placeholder_fix.py`
- **Type :** python
- **Taille :** 7.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 166
- **Hash MD5 :** `39373e4f8b81`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.15)*
  - ❓ `import_module` → `inspect` *(l.16)*
  - ❓ `import_module` → `re` *(l.18)*
  - ❓ `import_module` → `pytest` *(l.19)*
  - ✅ `import_module` → `tests` *(l.32)*
  - ❓ `import_module` → `tests.test_env_config` *(l.46)*
  - ❓ `import_module` → `src.ui.ci_status` *(l.69)*

### `agent-multiloop-Gabriel-local\tests\test_ci_status.py`
- **Type :** python
- **Taille :** 2.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 60
- **Hash MD5 :** `1ce859c1d380`
- **Références sortantes (10) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `os` *(l.3)*
  - ❓ `import_module` → `subprocess` *(l.5)*
  - ❓ `import_module` → `sys` *(l.6)*
  - ❓ `import_module` → `pathlib` *(l.7)*
  - ❓ `import_module` → `pytest` *(l.8)*
  - ❓ `import_module` → `src.ui.ci_status` *(l.10)*
  - ❓ `import_module` → `src.ui` *(l.54)*
  - ❓ `Path()` → `/nonexistent/tests/path` *(l.55)*
  - ❓ `chemin_litteral` → `test_dummy.py` *(l.37)*

### `agent-multiloop-Gabriel-local\tests\test_cognitive.py`
- **Type :** python
- **Taille :** 7.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 205
- **Hash MD5 :** `60a5d47e3eea`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `pathlib` *(l.3)*
  - ❓ `import_module` → `pytest` *(l.5)*
  - ❓ `import_module` → `src.cognitive` *(l.7)*
  - ❓ `import_module` → `src.cognitive.epistemic` *(l.14)*
  - ❓ `chemin_litteral` → `stats.json` *(l.149)*
  - ❓ `chemin_litteral` → `s.json` *(l.194)*

### `agent-multiloop-Gabriel-local\tests\test_composite_absurdity.py`
- **Type :** python
- **Taille :** 13.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 362
- **Hash MD5 :** `803044dca400`
- **Références sortantes (11) :**
  - ❓ `import_module` → `__future__` *(l.13)*
  - ❓ `import_module` → `asyncio` *(l.14)*
  - ❓ `import_module` → `sys` *(l.16)*
  - ❓ `import_module` → `pathlib` *(l.17)*
  - ❓ `import_module` → `unittest.mock` *(l.18)*
  - ❓ `import_module` → `pytest` *(l.19)*
  - ❓ `import_module` → `src.spectral.composite_absurdity_prover` *(l.24)*
  - ❓ `import_module` → `src.core.pipeline_with_gap_detection` *(l.218)*
  - ❓ `import_module` → `src.core.types` *(l.225)*
  - ❓ `import_module` → `re` *(l.312)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.171)*

### `agent-multiloop-Gabriel-local\tests\test_conversation_libre_savard.py`
- **Type :** python
- **Taille :** 3.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 85
- **Hash MD5 :** `2f99b4fde208`
- **Références sortantes (5) :**
  - ❓ `import_module` → `__future__` *(l.5)*
  - ❓ `import_module` → `pytest` *(l.6)*
  - ❓ `import_module` → `src.spectral.spectral_knowledge` *(l.14)*
  - ❓ `import_module` → `src.engines.meta_reasoning.meta_reasoning` *(l.57)*
  - ❓ `import_module` → `src.core.types` *(l.58)*

### `agent-multiloop-Gabriel-local\tests\test_conversational_memory.py`
- **Type :** python
- **Taille :** 14.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 381
- **Hash MD5 :** `ffd87870a23a`
- **Références sortantes (13) :**
  - ❓ `import_module` → `__future__` *(l.11)*
  - ❓ `import_module` → `asyncio` *(l.12)*
  - ❓ `import_module` → `sys` *(l.14)*
  - ❓ `import_module` → `pathlib` *(l.15)*
  - ❓ `import_module` → `unittest.mock` *(l.16)*
  - ❓ `import_module` → `pytest` *(l.17)*
  - ❓ `import_module` → `src.core.conversational_memory` *(l.22)*
  - ❓ `import_module` → `src.core.llm_manager` *(l.191)*
  - ❓ `import_module` → `src.core.orchestrator` *(l.256)*
  - ❓ `import_module` → `src.multiloop.refinement_loop` *(l.320)*
  - ❓ `import_module` → `src.core.types` *(l.321)*
  - ❓ `import_module` → `inspect` *(l.364)*
  - ❓ `import_module` → `src.multiloop` *(l.365)*

### `agent-multiloop-Gabriel-local\tests\test_conversational_memory_e2e.py`
- **Type :** python
- **Taille :** 7.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 211
- **Hash MD5 :** `cc130cc89867`
- **Références sortantes (9) :**
  - ❓ `import_module` → `__future__` *(l.6)*
  - ❓ `import_module` → `asyncio` *(l.7)*
  - ❓ `import_module` → `sys` *(l.9)*
  - ❓ `import_module` → `pathlib` *(l.10)*
  - ❓ `import_module` → `unittest.mock` *(l.11)*
  - ❓ `import_module` → `pytest` *(l.12)*
  - ❓ `import_module` → `src.core.llm_manager` *(l.22)*
  - ❓ `import_module` → `src.core.orchestrator` *(l.153)*
  - ❓ `import_module` → `src.core.conversational_memory` *(l.160)*

### `agent-multiloop-Gabriel-local\tests\test_conversational_mode.py`
- **Type :** python
- **Taille :** 7.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 184
- **Hash MD5 :** `6a50f66cd9eb`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.19)*
  - ❓ `import_module` → `sys` *(l.20)*
  - ❓ `import_module` → `pathlib` *(l.22)*
  - ❓ `import_module` → `pytest` *(l.23)*
  - ❓ `import_module` → `src.multiloop.request_decomposer` *(l.28)*
  - ❓ `import_module` → `src.core.pipeline` *(l.83)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\src\core\pipeline.py` *(l.88)*

### `agent-multiloop-Gabriel-local\tests\test_critic_vocab_and_gestionnaire_fix.py`
- **Type :** python
- **Taille :** 6.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 164
- **Hash MD5 :** `1cb56ea7233f`
- **Références sortantes (8) :**
  - ❓ `import_module` → `__future__` *(l.14)*
  - ❓ `import_module` → `sys` *(l.15)*
  - ❓ `import_module` → `pathlib` *(l.17)*
  - ❓ `import_module` → `unittest.mock` *(l.18)*
  - ❓ `import_module` → `pytest` *(l.19)*
  - ❓ `import_module` → `src.multiloop.critic` *(l.34)*
  - ❓ `import_module` → `src.core.types` *(l.42)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\src\core\llm_manager.py` *(l.133)*

### `agent-multiloop-Gabriel-local\tests\test_debat_orchestrator.py`
- **Type :** python
- **Taille :** 15.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 369
- **Hash MD5 :** `d14ecc80640a`
- **Références sortantes (10) :**
  - ❓ `import_module` → `__future__` *(l.6)*
  - ❓ `import_module` → `asyncio` *(l.7)*
  - ❓ `import_module` → `json` *(l.9)*
  - ❓ `import_module` → `pathlib` *(l.10)*
  - ❓ `import_module` → `unittest.mock` *(l.11)*
  - ❓ `import_module` → `pytest` *(l.12)*
  - ❓ `import_module` → `src.multiloop.debat_orchestrator` *(l.14)*
  - ❓ `import_module` → `re` *(l.251)*
  - ❓ `import_module` → `src.ui.cli` *(l.361)*
  - ❓ `Path()` → `data/debats` *(l.342)*

### `agent-multiloop-Gabriel-local\tests\test_debug_session.py`
- **Type :** python
- **Taille :** 6.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 180
- **Hash MD5 :** `9c86e478a5f4`
- **Références sortantes (10) :**
  - ❓ `import_module` → `__future__` *(l.11)*
  - ❓ `import_module` → `asyncio` *(l.12)*
  - ❓ `import_module` → `sys` *(l.14)*
  - ❓ `import_module` → `pathlib` *(l.15)*
  - ❓ `import_module` → `unittest.mock` *(l.16)*
  - ❓ `import_module` → `pytest` *(l.17)*
  - ❓ `import_module` → `rich.console` *(l.22)*
  - ❓ `import_module` → `src.ui.debug_session` *(l.24)*
  - ❓ `import_module` → `src.adapters.corpus.certainty_kernel` *(l.34)*
  - ❓ `import_module` → `src.core.spectral_core` *(l.35)*

### `agent-multiloop-Gabriel-local\tests\test_debug_toolkit.py`
- **Type :** python
- **Taille :** 5.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 180
- **Hash MD5 :** `6ca391857aaf`
- **Références sortantes (8) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `sys` *(l.3)*
  - ❓ `import_module` → `pathlib` *(l.5)*
  - ❓ `import_module` → `pytest` *(l.6)*
  - ❓ `import_module` → `src.debug_toolkit` *(l.11)*
  - ❓ `import_module` → `src.spectral.prime_table` *(l.15)*
  - ❓ `import_module` → `mpmath` *(l.95)*
  - ❓ `chemin_litteral` → `z3-solver devrait etre installe via requirements.txt` *(l.28)*

### `agent-multiloop-Gabriel-local\tests\test_dictionnaire_rag.py`
- **Type :** python
- **Taille :** 9.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 218
- **Hash MD5 :** `3abc54985e8e`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `fractions` *(l.3)*
  - ❓ `import_module` → `pytest` *(l.5)*
  - ✅ `import_module` → `memory` *(l.7)*
  - ❓ `import_module` → `memory.dictionnaire_spectral` *(l.16)*
  - ❓ `import_module` → `memory.adaptateur_cognitif_rag` *(l.214)*

### `agent-multiloop-Gabriel-local\tests\test_dictionnaire_rag_bq_integration.py`
- **Type :** python
- **Taille :** 5.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 141
- **Hash MD5 :** `bd3ecf791257`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.8)*
  - ❓ `import_module` → `re` *(l.9)*
  - ❓ `import_module` → `sys` *(l.11)*
  - ❓ `import_module` → `pathlib` *(l.12)*
  - ❓ `import_module` → `pytest` *(l.13)*
  - ❓ `import_module` → `memory.dictionnaire_spectral` *(l.18)*

### `agent-multiloop-Gabriel-local\tests\test_digamma_pure_v338.py`
- **Type :** python
- **Taille :** 4.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 123
- **Hash MD5 :** `585a82b70b54`
- **Références sortantes (5) :**
  - ❓ `import_module` → `__future__` *(l.9)*
  - ❓ `import_module` → `pytest` *(l.10)*
  - ❓ `import_module` → `fractions` *(l.12)*
  - ❓ `import_module` → `src.spectral.digamma_pure` *(l.13)*
  - ❓ `import_module` → `scipy.special` *(l.73)*

### `agent-multiloop-Gabriel-local\tests\test_domaine_sommes_XIA_v339.py`
- **Type :** python
- **Taille :** 6.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 163
- **Hash MD5 :** `2fc74c86f5b1`
- **Références sortantes (5) :**
  - ❓ `import_module` → `__future__` *(l.19)*
  - ❓ `import_module` → `re` *(l.20)*
  - ❓ `import_module` → `pathlib` *(l.22)*
  - ❓ `import_module` → `pytest` *(l.23)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.27)*

### `agent-multiloop-Gabriel-local\tests\test_engine_bridge.py`
- **Type :** python
- **Taille :** 6.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 184
- **Hash MD5 :** `aa54901b103e`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.9)*
  - ❓ `import_module` → `tempfile` *(l.10)*
  - ❓ `import_module` → `pathlib` *(l.12)*
  - ❓ `import_module` → `pytest` *(l.13)*
  - ❓ `import_module` → `src.cognitive` *(l.15)*
  - ❓ `import_module` → `src.cognitive.engine_bridge` *(l.26)*
  - ❓ `import_module` → `fractions` *(l.101)*

### `agent-multiloop-Gabriel-local\tests\test_env_config.py`
- **Type :** python
- **Taille :** 4.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 123
- **Hash MD5 :** `de19f456341b`
- **Références sortantes (8) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `os` *(l.3)*
  - ❓ `import_module` → `pathlib` *(l.5)*
  - ❓ `import_module` → `pytest` *(l.6)*
  - ❓ `import_module` → `src.core` *(l.8)*
  - ❓ `Path()` → `/app/agent-multiloop-Gabriel-local` *(l.25)*
  - ❓ `Path()` → `/home/agent/app` *(l.26)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\CONFIG_ENV_GUIDE.md` *(l.100)*

### `agent-multiloop-Gabriel-local\tests\test_extract_numbers_unicode_v346.py`
- **Type :** python
- **Taille :** 2.7 Ko
- **Modifié :** 2026-08-05 21:06:07
- **Lignes :** 61
- **Hash MD5 :** `10bbe1ebb412`
- **Références sortantes (6) :**
  - ❓ `import_module` → `re` *(l.3)*
  - ❓ `import_module` → `time` *(l.4)*
  - ❓ `import_module` → `pytest` *(l.5)*
  - ❓ `import_module` → `src.engines.abstraction.abstraction_layer` *(l.6)*
  - ❓ `import_module` → `pathlib` *(l.53)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\src\engines\abstraction\abstraction_layer.py` *(l.54)*

### `agent-multiloop-Gabriel-local\tests\test_filesystem_access.py`
- **Type :** python
- **Taille :** 8.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 223
- **Hash MD5 :** `3844905e7796`
- **Références sortantes (19) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `os` *(l.3)*
  - ❓ `import_module` → `struct` *(l.5)*
  - ❓ `import_module` → `zlib` *(l.6)*
  - ❓ `import_module` → `pathlib` *(l.7)*
  - ❓ `import_module` → `pytest` *(l.8)*
  - ❓ `import_module` → `src.core` *(l.10)*
  - ❓ `import_module` → `src.core.plan_trifocal_avec_image` *(l.12)*
  - ❓ `import_module` → `PIL` *(l.20)*
  - ❓ `chemin_litteral` → `test.md` *(l.30)*
  - ❓ `chemin_litteral` → `n_existe_pas.txt` *(l.49)*
  - ❓ `chemin_litteral` → `C:\\sub\\test.md` *(l.70)*
  - ❓ `chemin_litteral` → `programme.py` *(l.93)*
  - ❓ `chemin_litteral` → `enorme.md` *(l.101)*
  - ❓ `chemin_litteral` → `grand.txt` *(l.112)*
  - ❓ `chemin_litteral` → `a.txt` *(l.125)*
  - ❓ `chemin_litteral` → `fichier.txt` *(l.138)*
  - ❓ `chemin_litteral` → `a.md` *(l.210)*
  - ❓ `chemin_litteral` → `t.py` *(l.218)*

### `agent-multiloop-Gabriel-local\tests\test_forbidden_vocab_centralized.py`
- **Type :** python
- **Taille :** 9.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 213
- **Hash MD5 :** `0b3a2efbfb5d`
- **Références sortantes (11) :**
  - ❓ `import_module` → `__future__` *(l.17)*
  - ❓ `import_module` → `re` *(l.18)*
  - ❓ `import_module` → `pathlib` *(l.20)*
  - ❓ `import_module` → `pytest` *(l.21)*
  - ❓ `import_module` → `src.multiloop.forbidden_vocab` *(l.23)*
  - ❓ `chemin_litteral` → `src/multiloop/critic.py` *(l.133)*
  - ❓ `chemin_litteral` → `src/multiloop/coherence_detector.py` *(l.143)*
  - ❓ `chemin_litteral` → `src/core/spectral_core.py` *(l.153)*
  - ❓ `chemin_litteral` → `src/adapters/corpus/certainty_kernel.py` *(l.173)*
  - ❓ `chemin_litteral` → `src/multiloop/slow_motion_debugger.py` *(l.190)*
  - ❓ `chemin_litteral` → `src/spectral/spectral_knowledge.py` *(l.208)*

### `agent-multiloop-Gabriel-local\tests\test_gabriel_certification.py`
- **Type :** python
- **Taille :** 13.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 302
- **Hash MD5 :** `8f426297ef97`
- **Références sortantes (5) :**
  - ❓ `import_module` → `pytest` *(l.10)*
  - ❓ `import_module` → `src.spectral.gap_solver_corrected` *(l.12)*
  - ❓ `import_module` → `src.spectral.prime_table` *(l.13)*
  - ❓ `import_module` → `src.adapters.hol_isabelle.isabelle_adapter` *(l.14)*
  - ❓ `import_module` → `src.adapters.llm.utf8_sanitizer` *(l.15)*

### `agent-multiloop-Gabriel-local\tests\test_gabriel_v52_hol_formal.py`
- **Type :** python
- **Taille :** 7.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 158
- **Hash MD5 :** `7b1b6ae697cb`
- **Références sortantes (5) :**
  - ❓ `import_module` → `__future__` *(l.9)*
  - ❓ `import_module` → `pytest` *(l.10)*
  - ❓ `import_module` → `src.hol_isabelle_formal_generator` *(l.22)*
  - ❓ `import_module` → `memory.prompt_injector_enhanced` *(l.90)*
  - ❓ `import_module` → `src.gabriel_llm_integration_safe` *(l.143)*

### `agent-multiloop-Gabriel-local\tests\test_gap_compute.py`
- **Type :** python
- **Taille :** 3.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 98
- **Hash MD5 :** `0cae97bc95fa`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `sys` *(l.3)*
  - ❓ `import_module` → `pathlib` *(l.5)*
  - ❓ `import_module` → `pytest` *(l.6)*
  - ❓ `import_module` → `src.spectral.gap_compute` *(l.11)*
  - ❓ `import_module` → `src.spectral.prime_table` *(l.13)*

### `agent-multiloop-Gabriel-local\tests\test_gap_solver_mixed_negative_positive.py`
- **Type :** python
- **Taille :** 7.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 186
- **Hash MD5 :** `0b18a0e66dfd`
- **Références sortantes (5) :**
  - ❓ `import_module` → `__future__` *(l.13)*
  - ❓ `import_module` → `sys` *(l.14)*
  - ❓ `import_module` → `pathlib` *(l.16)*
  - ❓ `import_module` → `pytest` *(l.17)*
  - ❓ `import_module` → `src.spectral.gap_solver_corrected` *(l.22)*

### `agent-multiloop-Gabriel-local\tests\test_generic_prime_i_query.py`
- **Type :** python
- **Taille :** 4.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 112
- **Hash MD5 :** `37fa30ce1ca5`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.8)*
  - ❓ `import_module` → `sys` *(l.9)*
  - ❓ `import_module` → `pathlib` *(l.11)*
  - ❓ `import_module` → `pytest` *(l.12)*
  - ❓ `import_module` → `src.multiloop.request_decomposer` *(l.17)*
  - ❓ `import_module` → `src.multiloop.slow_motion_debugger` *(l.65)*

### `agent-multiloop-Gabriel-local\tests\test_geometrie_spectrale_engine.py`
- **Type :** python
- **Taille :** 10.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 294
- **Hash MD5 :** `95ce27e8dcf9`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.9)*
  - ❓ `import_module` → `fractions` *(l.10)*
  - ❓ `import_module` → `pytest` *(l.12)*
  - ❓ `import_module` → `src.core.spectral_core` *(l.14)*
  - ❓ `import_module` → `src.engines.geometrie_spectrale_engine` *(l.16)*
  - ❓ `import_module` → `src.spectral.spectral_models` *(l.20)*

### `agent-multiloop-Gabriel-local\tests\test_geometrie_tex_pasj02_fix.py`
- **Type :** python
- **Taille :** 9.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 257
- **Hash MD5 :** `3846dd7e0d34`
- **Références sortantes (5) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `re` *(l.3)*
  - ❓ `import_module` → `unicodedata` *(l.5)*
  - ❓ `import_module` → `pathlib` *(l.6)*
  - ❓ `import_module` → `pytest` *(l.7)*

### `agent-multiloop-Gabriel-local\tests\test_graph_enrichment_v325.py`
- **Type :** python
- **Taille :** 7.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 197
- **Hash MD5 :** `66b35cd9d02e`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.14)*
  - ❓ `import_module` → `pytest` *(l.15)*
  - ❓ `import_module` → `src.core.spectral_core` *(l.17)*
  - ❓ `import_module` → `src.visualization.curves` *(l.19)*

### `agent-multiloop-Gabriel-local\tests\test_image_command_windows_routing.py`
- **Type :** python
- **Taille :** 6.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 213
- **Hash MD5 :** `05c9d912a2fc`
- **Références sortantes (15) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `io` *(l.3)*
  - ❓ `import_module` → `re` *(l.5)*
  - ❓ `import_module` → `pathlib` *(l.6)*
  - ❓ `import_module` → `pytest` *(l.7)*
  - ❓ `import_module` → `PIL` *(l.9)*
  - ❓ `import_module` → `rich.console` *(l.10)*
  - ❓ `import_module` → `src.core` *(l.11)*
  - ❓ `import_module` → `src.ui` *(l.13)*
  - ❓ `import_module` → `src.ui.cli` *(l.14)*
  - ❓ `Path()` → `/home/agent/app/data/theorie-savard/assets/images/figure.png` *(l.197)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\docker-compose.yml` *(l.107)*
  - ❓ `chemin_litteral` → `/tmp/figure.png` *(l.147)*
  - ❓ `chemin_litteral` → `fichier.txt` *(l.185)*
  - ❓ `chemin_litteral` → `c:/dossier/fichier.txt` *(l.190)*

### `agent-multiloop-Gabriel-local\tests\test_integrateur_memoire_api_fix.py`
- **Type :** python
- **Taille :** 6.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 145
- **Hash MD5 :** `ed7c217056c3`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.14)*
  - ❓ `import_module` → `pytest` *(l.15)*
  - ❓ `import_module` → `src.core.integrateur_memoire` *(l.17)*
  - ❓ `import_module` → `src.core.llm_manager` *(l.19)*
  - ❓ `import_module` → `inspect` *(l.67)*
  - ❓ `import_module` → `src.core` *(l.131)*

### `agent-multiloop-Gabriel-local\tests\test_isabelle_fixes_bugs_9_10.py`
- **Type :** python
- **Taille :** 4.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 109
- **Hash MD5 :** `22fe6bcda5b3`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.18)*
  - ❓ `import_module` → `re` *(l.19)*
  - ❓ `import_module` → `sys` *(l.21)*
  - ❓ `import_module` → `pathlib` *(l.22)*
  - ❓ `import_module` → `pytest` *(l.23)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.32)*

### `agent-multiloop-Gabriel-local\tests\test_isabelle_fixes_v321.py`
- **Type :** python
- **Taille :** 6.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 155
- **Hash MD5 :** `afd287b3075d`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.15)*
  - ❓ `import_module` → `sys` *(l.16)*
  - ❓ `import_module` → `pathlib` *(l.18)*
  - ❓ `import_module` → `pytest` *(l.19)*
  - ❓ `import_module` → `re` *(l.64)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.28)*

### `agent-multiloop-Gabriel-local\tests\test_isabelle_rsp_non_zero_witness.py`
- **Type :** python
- **Taille :** 4.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 103
- **Hash MD5 :** `5830a802d120`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.12)*
  - ❓ `import_module` → `re` *(l.13)*
  - ❓ `import_module` → `sys` *(l.15)*
  - ❓ `import_module` → `pathlib` *(l.16)*
  - ❓ `import_module` → `pytest` *(l.17)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.26)*

### `agent-multiloop-Gabriel-local\tests\test_keybindings.py`
- **Type :** python
- **Taille :** 2.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 70
- **Hash MD5 :** `5f8c5d06f43b`
- **Références sortantes (5) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `pathlib` *(l.3)*
  - ❓ `import_module` → `src.ui.keybindings` *(l.5)*
  - ❓ `chemin_litteral` → `/tmp/test_gabriel_history_xyz` *(l.55)*
  - ❓ `chemin_litteral` → `/tmp/different_path_ignored` *(l.58)*

### `agent-multiloop-Gabriel-local\tests\test_latex_healthcheck.py`
- **Type :** python
- **Taille :** 4.0 Ko
- **Modifié :** 2026-08-05 21:06:07
- **Lignes :** 110
- **Hash MD5 :** `14c7e9387d71`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `re` *(l.3)*
  - ❓ `import_module` → `pathlib` *(l.5)*
  - ❓ `import_module` → `pytest` *(l.6)*

### `agent-multiloop-Gabriel-local\tests\test_lean_methode_spectrale_port.py`
- **Type :** python
- **Taille :** 22.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 559
- **Hash MD5 :** `3ac05ee1fdb8`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.11)*
  - ❓ `import_module` → `sys` *(l.12)*
  - ❓ `import_module` → `pathlib` *(l.14)*
  - ❓ `import_module` → `pytest` *(l.15)*

### `agent-multiloop-Gabriel-local\tests\test_llm_reformulator.py`
- **Type :** python
- **Taille :** 10.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 274
- **Hash MD5 :** `a374f2f4a414`
- **Références sortantes (8) :**
  - ❓ `import_module` → `__future__` *(l.16)*
  - ❓ `import_module` → `asyncio` *(l.17)*
  - ❓ `import_module` → `unittest.mock` *(l.19)*
  - ❓ `import_module` → `pytest` *(l.20)*
  - ❓ `import_module` → `src.multiloop.llm_reformulator` *(l.22)*
  - ❓ `import_module` → `src.multiloop.request_decomposer` *(l.28)*
  - ❓ `import_module` → `inspect` *(l.264)*
  - ❓ `import_module` → `src.multiloop.slow_motion_debugger` *(l.265)*

### `agent-multiloop-Gabriel-local\tests\test_logging_setup_esthetique.py`
- **Type :** python
- **Taille :** 5.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 161
- **Hash MD5 :** `269206db8e9a`
- **Références sortantes (9) :**
  - ❓ `import_module` → `__future__` *(l.11)*
  - ❓ `import_module` → `logging` *(l.12)*
  - ❓ `import_module` → `os` *(l.14)*
  - ❓ `import_module` → `sys` *(l.15)*
  - ❓ `import_module` → `pathlib` *(l.16)*
  - ❓ `import_module` → `pytest` *(l.17)*
  - ❓ `import_module` → `src.core.logging_setup` *(l.22)*
  - ❓ `import_module` → `importlib` *(l.124)*
  - ❓ `import_module` → `time` *(l.132)*

### `agent-multiloop-Gabriel-local\tests\test_mandatory_questions.py`
- **Type :** python
- **Taille :** 7.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 206
- **Hash MD5 :** `a49e7598f761`
- **Références sortantes (5) :**
  - ❓ `import_module` → `fractions` *(l.8)*
  - ❓ `import_module` → `pytest` *(l.9)*
  - ❓ `import_module` → `src.spectral` *(l.11)*
  - ❓ `import_module` → `src.core.types` *(l.21)*
  - ❓ `import_module` → `src.spectral.gaps` *(l.184)*

### `agent-multiloop-Gabriel-local\tests\test_methode_spectral_healthcheck.py`
- **Type :** python
- **Taille :** 6.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 162
- **Hash MD5 :** `99770eb95c7e`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.7)*
  - ❓ `import_module` → `re` *(l.8)*
  - ❓ `import_module` → `sys` *(l.10)*
  - ❓ `import_module` → `pathlib` *(l.11)*
  - ❓ `import_module` → `pytest` *(l.12)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\theories\verify_thy_structure.py` *(l.18)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.16)*

### `agent-multiloop-Gabriel-local\tests\test_paths_resolution_container_fix.py`
- **Type :** python
- **Taille :** 7.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 159
- **Hash MD5 :** `c7d43d0be42f`
- **Références sortantes (16) :**
  - ❓ `import_module` → `__future__` *(l.25)*
  - ❓ `import_module` → `pathlib` *(l.26)*
  - ❓ `import_module` → `pytest` *(l.28)*
  - ❓ `import_module` → `inspect` *(l.39)*
  - ✅ `import_module` → `tests` *(l.40)*
  - ❓ `import_module` → `tests.test_env_config` *(l.88)*
  - ❓ `import_module` → `tests.test_slow_motion_debugger` *(l.100)*
  - ❓ `import_module` → `tests.test_section_XI_XII_integration` *(l.106)*
  - ❓ `Path()` → `/app/agent-multiloop-Gabriel-local/CONFIG_ENV_GUIDE.md` *(l.13)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\CONFIG_ENV_GUIDE.md` *(l.57)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.107)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\docker-compose.yml` *(l.128)*
  - ❓ `chemin_litteral` → `/home/agent/app/theories` *(l.135)*
  - ❓ `chemin_litteral` → `/home/agent/app/theories pour la coherence des tests.` *(l.137)*
  - ❓ `chemin_litteral` → `/home/agent/app/scripts` *(l.149)*
  - ❓ `chemin_litteral` → `/home/agent/app/memory` *(l.156)*

### `agent-multiloop-Gabriel-local\tests\test_philippe_three_categories_v329.py`
- **Type :** python
- **Taille :** 4.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 129
- **Hash MD5 :** `1e9aab556468`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.8)*
  - ❓ `import_module` → `pytest` *(l.9)*
  - ❓ `import_module` → `src.core.spectral_core` *(l.11)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.66)*

### `agent-multiloop-Gabriel-local\tests\test_pipeline_epistemic.py`
- **Type :** python
- **Taille :** 3.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 77
- **Hash MD5 :** `3dfac4cdec8c`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `tempfile` *(l.3)*
  - ❓ `import_module` → `pytest` *(l.5)*
  - ❓ `import_module` → `src.core.types` *(l.7)*
  - ❓ `import_module` → `src.cognitive` *(l.9)*
  - ❓ `import_module` → `src.core.pipeline` *(l.23)*

### `agent-multiloop-Gabriel-local\tests\test_plan_trifocal.py`
- **Type :** python
- **Taille :** 6.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 167
- **Hash MD5 :** `bb5b3465faaa`
- **Références sortantes (5) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `fractions` *(l.3)*
  - ❓ `import_module` → `pytest` *(l.5)*
  - ❓ `import_module` → `src.spectral` *(l.7)*
  - ❓ `import_module` → `src.cognitive` *(l.141)*

### `agent-multiloop-Gabriel-local\tests\test_pre_reasoner_v334.py`
- **Type :** python
- **Taille :** 12.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 315
- **Hash MD5 :** `3717c89ba10f`
- **Références sortantes (8) :**
  - ❓ `import_module` → `__future__` *(l.14)*
  - ❓ `import_module` → `pytest` *(l.15)*
  - ❓ `import_module` → `src.multiloop.pre_reasoner` *(l.17)*
  - ❓ `chemin_litteral` → `/rapide résume la section XIII` *(l.227)*
  - ❓ `chemin_litteral` → `/standard calcule RsP(5,7)` *(l.232)*
  - ❓ `chemin_litteral` → `/approfondi symétrique 3x3` *(l.237)*
  - ❓ `chemin_litteral` → `/complet zeta et Riemann` *(l.242)*
  - ❓ `chemin_litteral` → `/rapide` *(l.252)*

### `agent-multiloop-Gabriel-local\tests\test_psi_savard_pont_zeta_v331.py`
- **Type :** python
- **Taille :** 9.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 219
- **Hash MD5 :** `f7ec41027d3c`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.13)*
  - ❓ `import_module` → `math` *(l.14)*
  - ❓ `import_module` → `re` *(l.16)*
  - ❓ `import_module` → `pathlib` *(l.17)*
  - ❓ `import_module` → `pytest` *(l.18)*
  - ❓ `import_module` → `src.core.spectral_core` *(l.20)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.24)*

### `agent-multiloop-Gabriel-local\tests\test_psi_savard_v340.py`
- **Type :** python
- **Taille :** 4.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 146
- **Hash MD5 :** `5b9b76cb678b`
- **Références sortantes (4) :**
  - ❓ `import_module` → `__future__` *(l.14)*
  - ❓ `import_module` → `math` *(l.15)*
  - ❓ `import_module` → `pytest` *(l.17)*
  - ❓ `import_module` → `src.spectral.psi_savard` *(l.18)*

### `agent-multiloop-Gabriel-local\tests\test_restore_methode_spectral_0f277b5.py`
- **Type :** python
- **Taille :** 3.6 Ko
- **Modifié :** 2026-08-15 00:15:16
- **Lignes :** 107
- **Hash MD5 :** `2bbba351ddf4`
- **Références sortantes (8) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `hashlib` *(l.3)*
  - ❓ `import_module` → `subprocess` *(l.5)*
  - ❓ `import_module` → `unicodedata` *(l.6)*
  - ❓ `import_module` → `pathlib` *(l.7)*
  - ❓ `import_module` → `pytest` *(l.8)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.14)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.15)*

### `agent-multiloop-Gabriel-local\tests\test_rsp_command.py`
- **Type :** python
- **Taille :** 4.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 145
- **Hash MD5 :** `ce5a8047f09e`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `sys` *(l.3)*
  - ❓ `import_module` → `pathlib` *(l.5)*
  - ❓ `import_module` → `pytest` *(l.6)*
  - ❓ `import_module` → `src.core.spectral_core` *(l.11)*
  - ❓ `import_module` → `src.spectral.rsp_command` *(l.13)*
  - ❓ `import_module` → `random` *(l.98)*

### `agent-multiloop-Gabriel-local\tests\test_rsp_curve.py`
- **Type :** python
- **Taille :** 2.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 82
- **Hash MD5 :** `69180abef028`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `sys` *(l.3)*
  - ❓ `import_module` → `pathlib` *(l.5)*
  - ❓ `import_module` → `pytest` *(l.6)*
  - ❓ `import_module` → `src.core.spectral_core` *(l.11)*
  - ❓ `import_module` → `src.spectral.rsp_curve` *(l.13)*

### `agent-multiloop-Gabriel-local\tests\test_section_XI_XII_integration.py`
- **Type :** python
- **Taille :** 9.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 210
- **Hash MD5 :** `01385f6d69c2`
- **Références sortantes (18) :**
  - ❓ `import_module` → `__future__` *(l.12)*
  - ❓ `import_module` → `fractions` *(l.13)*
  - ❓ `import_module` → `pathlib` *(l.14)*
  - ❓ `import_module` → `subprocess` *(l.15)*
  - ❓ `import_module` → `sys` *(l.16)*
  - ❓ `import_module` → `pytest` *(l.17)*
  - ❓ `import_module` → `os` *(l.30)*
  - ❓ `import_module` → `memory.methode_spectral_section_XII` *(l.52)*
  - ❓ `import_module` → `memory.methode_spectral_section_XI` *(l.137)*
  - ❓ `import_module` → `memory.dictionnaire_spectral` *(l.154)*
  - ❓ `import_module` → `memory.adaptateur_cognitif_rag` *(l.167)*
  - ❓ `Path()` → `/theories` *(l.34)*
  - ❓ `Path()` → `/home/agent/app/theories` *(l.35)*
  - ❓ `Path()` → `/app/agent-multiloop-Gabriel-local/theories` *(l.36)*
  - ❓ `Path()` → `/home/agent/app/scripts/isabelle_static_check.py` *(l.198)*
  - ❓ `Path()` → `/app/agent-multiloop-Gabriel-local/scripts/isabelle_static_check.py` *(l.199)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.23)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\scripts\isabelle_static_check.py` *(l.197)*

### `agent-multiloop-Gabriel-local\tests\test_section_xiii_professionnelle_v332.py`
- **Type :** python
- **Taille :** 7.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 179
- **Hash MD5 :** `1c4768355f23`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.19)*
  - ❓ `import_module` → `math` *(l.20)*
  - ❓ `import_module` → `re` *(l.22)*
  - ❓ `import_module` → `pathlib` *(l.23)*
  - ❓ `import_module` → `pytest` *(l.24)*
  - ❓ `import_module` → `src.core.spectral_core` *(l.26)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.30)*

### `agent-multiloop-Gabriel-local\tests\test_section_xiii_rag_v333.py`
- **Type :** python
- **Taille :** 10.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 251
- **Hash MD5 :** `f9c4771d433e`
- **Références sortantes (10) :**
  - ❓ `import_module` → `__future__` *(l.14)*
  - ❓ `import_module` → `math` *(l.15)*
  - ❓ `import_module` → `pytest` *(l.17)*
  - ❓ `import_module` → `memory.dictionnaire_spectral` *(l.19)*
  - ❓ `import_module` → `memory.adaptateur_cognitif_rag` *(l.26)*
  - ❓ `import_module` → `memory.methode_spectral_section_XIII` *(l.27)*
  - ❓ `import_module` → `sys` *(l.232)*
  - ❓ `import_module` → `pathlib` *(l.233)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` *(l.236)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.55)*

### `agent-multiloop-Gabriel-local\tests\test_silent_audit.py`
- **Type :** python
- **Taille :** 7.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 205
- **Hash MD5 :** `b4574603b8b4`
- **Références sortantes (8) :**
  - ❓ `import_module` → `__future__` *(l.11)*
  - ❓ `import_module` → `asyncio` *(l.12)*
  - ❓ `import_module` → `sys` *(l.14)*
  - ❓ `import_module` → `pathlib` *(l.15)*
  - ❓ `import_module` → `pytest` *(l.16)*
  - ❓ `import_module` → `src.core.spectral_core` *(l.22)*
  - ❓ `import_module` → `src.core.types` *(l.24)*
  - ❓ `import_module` → `src.multiloop.silent_audit` *(l.25)*

### `agent-multiloop-Gabriel-local\tests\test_slow_motion_debugger.py`
- **Type :** python
- **Taille :** 12.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 350
- **Hash MD5 :** `fcdecb6b2697`
- **Références sortantes (14) :**
  - ❓ `import_module` → `__future__` *(l.10)*
  - ❓ `import_module` → `sys` *(l.11)*
  - ❓ `import_module` → `pathlib` *(l.13)*
  - ❓ `import_module` → `pytest` *(l.14)*
  - ❓ `import_module` → `src.adapters.corpus.certainty_kernel` *(l.19)*
  - ❓ `import_module` → `src.core.spectral_core` *(l.21)*
  - ❓ `import_module` → `src.core.types` *(l.22)*
  - ❓ `import_module` → `src.multiloop.coherence_detector` *(l.23)*
  - ❓ `import_module` → `src.multiloop.request_decomposer` *(l.24)*
  - ❓ `import_module` → `src.multiloop.slow_motion_debugger` *(l.25)*
  - ❓ `import_module` → `os` *(l.30)*
  - ❓ `Path()` → `/theories` *(l.36)*
  - ❓ `Path()` → `/home/agent/app/theories` *(l.37)*
  - ❓ `Path()` → `/app/agent-multiloop-Gabriel-local/theories` *(l.38)*

### `agent-multiloop-Gabriel-local\tests\test_slow_motion_improvements.py`
- **Type :** python
- **Taille :** 9.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 204
- **Hash MD5 :** `c6e063273e0c`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.9)*
  - ❓ `import_module` → `src.multiloop.request_decomposer` *(l.10)*
  - ❓ `import_module` → `src.multiloop.slow_motion_debugger` *(l.12)*
  - ❓ `import_module` → `src.multiloop.coherence_detector` *(l.13)*
  - ❓ `import_module` → `src.core.types` *(l.14)*
  - ❓ `import_module` → `src.adapters.corpus.certainty_kernel` *(l.116)*
  - ❓ `import_module` → `src.core.spectral_core` *(l.117)*

### `agent-multiloop-Gabriel-local\tests\test_spectral_family_foundations_v335.py`
- **Type :** python
- **Taille :** 12.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 277
- **Hash MD5 :** `d282a3e8fd0b`
- **Références sortantes (5) :**
  - ❓ `import_module` → `__future__` *(l.27)*
  - ❓ `import_module` → `re` *(l.28)*
  - ❓ `import_module` → `pathlib` *(l.30)*
  - ❓ `import_module` → `pytest` *(l.31)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.34)*

### `agent-multiloop-Gabriel-local\tests\test_spectral_ratio_configurations.py`
- **Type :** python
- **Taille :** 6.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 171
- **Hash MD5 :** `48b55040214f`
- **Références sortantes (10) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `sys` *(l.3)*
  - ❓ `import_module` → `pathlib` *(l.5)*
  - ❓ `import_module` → `pytest` *(l.6)*
  - ❓ `import_module` → `src.core.spectral_core` *(l.11)*
  - ❓ `import_module` → `src.multiloop.request_decomposer` *(l.13)*
  - ❓ `import_module` → `rich.console` *(l.139)*
  - ❓ `import_module` → `src.adapters.corpus.certainty_kernel` *(l.140)*
  - ❓ `import_module` → `src.ui.debug_session` *(l.141)*
  - ❓ `import_module` → `unittest.mock` *(l.148)*

### `agent-multiloop-Gabriel-local\tests\test_splash_and_citations.py`
- **Type :** python
- **Taille :** 3.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 77
- **Hash MD5 :** `2a7205c221d2`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `pytest` *(l.3)*
  - ❓ `import_module` → `src.ui.cli` *(l.10)*
  - ❓ `import_module` → `rich.console` *(l.56)*
  - ❓ `import_module` → `io` *(l.57)*
  - ❓ `import_module` → `src.ui.keybindings` *(l.68)*

### `agent-multiloop-Gabriel-local\tests\test_timeout_and_extensions_v320.py`
- **Type :** python
- **Taille :** 7.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 199
- **Hash MD5 :** `56e8ad3fdb68`
- **Références sortantes (9) :**
  - ❓ `import_module` → `__future__` *(l.7)*
  - ❓ `import_module` → `re` *(l.8)*
  - ❓ `import_module` → `sys` *(l.10)*
  - ❓ `import_module` → `pathlib` *(l.11)*
  - ❓ `import_module` → `pytest` *(l.12)*
  - ❓ `import_module` → `src.visualization` *(l.75)*
  - ❓ `import_module` → `src.spectral.composite_absurdity_prover` *(l.183)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\config.yaml` *(l.25)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.113)*

### `agent-multiloop-Gabriel-local\tests\test_traced_calculations.py`
- **Type :** python
- **Taille :** 7.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 187
- **Hash MD5 :** `7eeeb019a3f2`
- **Références sortantes (5) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `json` *(l.3)*
  - ❓ `import_module` → `fractions` *(l.5)*
  - ❓ `import_module` → `pytest` *(l.6)*
  - ❓ `import_module` → `src.cognitive` *(l.8)*

### `agent-multiloop-Gabriel-local\tests\test_ui_pro_banner_and_memoire.py`
- **Type :** python
- **Taille :** 4.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 99
- **Hash MD5 :** `75e57b5847fa`
- **Références sortantes (11) :**
  - ❓ `import_module` → `__future__` *(l.7)*
  - ❓ `import_module` → `pytest` *(l.8)*
  - ❓ `import_module` → `src.ui.cli` *(l.15)*
  - ❓ `import_module` → `rich.console` *(l.20)*
  - ❓ `import_module` → `io` *(l.21)*
  - ❓ `import_module` → `sys` *(l.48)*
  - ❓ `import_module` → `pathlib` *(l.49)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` *(l.52)*
  - ❓ `import_module` → `src.core.llm_manager` *(l.80)*
  - ❓ `import_module` → `src.multiloop.request_decomposer` *(l.97)*
  - ❓ `chemin_litteral` → `emergent.sh` *(l.30)*

### `agent-multiloop-Gabriel-local\tests\test_unicode_surrogate_fix.py`
- **Type :** python
- **Taille :** 6.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 168
- **Hash MD5 :** `c1732ee73c3e`
- **Références sortantes (9) :**
  - ❓ `import_module` → `__future__` *(l.10)*
  - ❓ `import_module` → `asyncio` *(l.11)*
  - ❓ `import_module` → `json` *(l.13)*
  - ❓ `import_module` → `tempfile` *(l.14)*
  - ❓ `import_module` → `pathlib` *(l.15)*
  - ❓ `import_module` → `pytest` *(l.16)*
  - ❓ `import_module` → `src.adapters.llm.utf8_sanitizer` *(l.18)*
  - ❓ `import_module` → `src.audit` *(l.20)*
  - ❓ `import_module` → `src.core.llm_manager` *(l.132)*

### `agent-multiloop-Gabriel-local\tests\test_validation16_savard_and_build_workflow.py`
- **Type :** python
- **Taille :** 9.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 268
- **Hash MD5 :** `cfaf528bf6be`
- **Références sortantes (15) :**
  - ❓ `import_module` → `__future__` *(l.17)*
  - ❓ `import_module` → `sys` *(l.18)*
  - ❓ `import_module` → `pathlib` *(l.20)*
  - ❓ `import_module` → `pytest` *(l.21)*
  - ❓ `chemin_litteral` → `./theories` *(l.34)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.41)*
  - ❓ `chemin_litteral` → `La definition Savard `{name}` doit exister dans methode_spectral.thy` *(l.72)*
  - ❓ `chemin_litteral` → `Le lemme/theoreme `{name}` doit exister dans methode_spectral.thy` *(l.114)*
  - ❓ `chemin_litteral` → `Tactique Lean 4 interdite `{forbidden}` detectee dans .thy` *(l.185)*
  - ✅ `chemin_litteral` → `.github\workflows\build.yml` *(l.223)*
  - ✅ `chemin_litteral` → `.github` *(l.227)*
  - ❓ `chemin_litteral` → `elan-init.sh` *(l.246)*
  - ❓ `chemin_litteral` → `sha256sum theories/methode_spectral.thy` *(l.249)*
  - ❓ `chemin_litteral` → `theories/methode_spectral.thy` *(l.256)*
  - ❓ `chemin_litteral` → `SHA256SUMS.txt` *(l.261)*

### `agent-multiloop-Gabriel-local\tests\test_verification_loop.py`
- **Type :** python
- **Taille :** 6.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 194
- **Hash MD5 :** `94719395f18b`
- **Références sortantes (8) :**
  - ❓ `import_module` → `__future__` *(l.9)*
  - ❓ `import_module` → `sys` *(l.10)*
  - ❓ `import_module` → `pathlib` *(l.12)*
  - ❓ `import_module` → `pytest` *(l.13)*
  - ❓ `import_module` → `src.adapters.hol_isabelle.isabelle_adapter` *(l.18)*
  - ❓ `import_module` → `src.adapters.wolfram.wolfram_client` *(l.20)*
  - ❓ `import_module` → `src.audit` *(l.21)*
  - ❓ `import_module` → `src.multiloop.verification_loop` *(l.22)*

### `agent-multiloop-Gabriel-local\tests\test_verify_thy_structure.py`
- **Type :** python
- **Taille :** 13.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 348
- **Hash MD5 :** `d53809b24cdd`
- **Références sortantes (10) :**
  - ❓ `import_module` → `__future__` *(l.11)*
  - ❓ `import_module` → `json` *(l.12)*
  - ❓ `import_module` → `subprocess` *(l.14)*
  - ❓ `import_module` → `sys` *(l.15)*
  - ❓ `import_module` → `pathlib` *(l.16)*
  - ❓ `import_module` → `pytest` *(l.17)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\theories\verify_thy_structure.py` *(l.24)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\verify_thy_structure.py` *(l.22)*
  - ❓ `chemin_litteral` → `test.thy` *(l.35)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.340)*

### `agent-multiloop-Gabriel-local\tests\test_visualization.py`
- **Type :** python
- **Taille :** 7.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 212
- **Hash MD5 :** `677cdf5a6ae2`
- **Références sortantes (6) :**
  - ❓ `import_module` → `__future__` *(l.2)*
  - ❓ `import_module` → `pathlib` *(l.3)*
  - ❓ `import_module` → `pytest` *(l.5)*
  - ❓ `import_module` → `src.core.spectral_core` *(l.7)*
  - ❓ `import_module` → `src.visualization` *(l.9)*
  - ❓ `import_module` → `rich.table` *(l.157)*

### `agent-multiloop-Gabriel-local\tests\test_workflow_2025_2_contract.py`
- **Type :** python
- **Taille :** 1.8 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 47
- **Hash MD5 :** `87683aa497fd`
- **Références sortantes (6) :**
  - ❓ `import_module` → `pathlib` *(l.2)*
  - ❓ `import_module` → `re` *(l.3)*
  - ❓ `Path()` → `/home/agent/app/.github/workflows/build.yml` *(l.6)*
  - ❓ `chemin_litteral` → `/tmp/isabelle/Isabelle2025-2/bin` *(l.20)*
  - ❓ `chemin_litteral` → `/tmp/isabelle/Isabelle2025-2/bin/isabelle version` *(l.21)*
  - ❓ `chemin_litteral` → `subject-path: agent-multiloop-Gabriel-local/theories/methode_spectral.thy` *(l.41)*

### `agent-multiloop-Gabriel-local\tests\test_workflow_isabelle_syntax.py`
- **Type :** python
- **Taille :** 10.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 248
- **Hash MD5 :** `d92402e64e50`
- **Références sortantes (11) :**
  - ❓ `import_module` → `__future__` *(l.12)*
  - ❓ `import_module` → `sys` *(l.13)*
  - ❓ `import_module` → `pathlib` *(l.15)*
  - ❓ `import_module` → `pytest` *(l.16)*
  - ❓ `import_module` → `re` *(l.48)*
  - ❓ `Path()` → `/app` *(l.19)*
  - ❓ `chemin_litteral` → `*.yml` *(l.35)*
  - ❓ `chemin_litteral` → `isabelle\s+process\s+-T\s+\S+\.thy` *(l.49)*
  - ✅ `chemin_litteral` → `.github\workflows\build.yml` *(l.95)*
  - ❓ `chemin_litteral` → `src/hol/methode_spectral.thy` *(l.113)*
  - ❓ `chemin_litteral` → `theories/methode_spectral.thy` *(l.212)*

### `agent-multiloop-Gabriel-local\theories\MethodeSpectrale.lean`
- **Type :** autre
- **Taille :** 66.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 1582
- **Hash MD5 :** `5ece08de20be`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\PLAN_FACTORISATION_ET_META_THEORY.md`
- **Type :** markdown
- **Taille :** 15.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 280
- **Hash MD5 :** `6fe78180d9ef`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\README_LEAN.md`
- **Type :** markdown
- **Taille :** 3.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 81
- **Hash MD5 :** `31a7b7b0cab5`
- **Références sortantes (1) :**
  - ❓ `ref_generique` → `//raw.githubusercontent.com/leanprover/elan/master/elan-init.sh` *(l.20)*

### `agent-multiloop-Gabriel-local\theories\ROOT`
- **Type :** autre
- **Taille :** 171.0 o
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 8
- **Hash MD5 :** `3d4cbc057013`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\RiemannSpectral.lean`
- **Type :** autre
- **Taille :** 2.8 Ko
- **Modifié :** 2026-08-15 00:15:16
- **Lignes :** 93
- **Hash MD5 :** `5e27da77ba74`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\Words_docx\Géométrie du Spectre des Nombres Premiers — Brouillon Savard 2026.docx`
- **Type :** autre
- **Taille :** 48.1 Ko
- **Modifié :** 2026-08-05 21:06:07
- **Hash MD5 :** `f25f387f67eb`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\archive\methode_spectral_axiome_geometrique.thy`
- **Type :** isabelle
- **Taille :** 114.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 3047
- **Hash MD5 :** `82437a65b7fb`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\banque_qr\QR_Technique_Spectre_Nombres_Premiers (1).pdf`
- **Type :** autre
- **Taille :** 213.3 Ko
- **Modifié :** 2026-08-16 20:18:44
- **Hash MD5 :** `d655356ade39`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\geometrie_spectre_premier.thy`
- **Type :** isabelle
- **Taille :** 9.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 318
- **Hash MD5 :** `ebbcf9d8540a`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Complex_Main` *(l.1)*

### `agent-multiloop-Gabriel-local\theories\methode_spectral.thy`
- **Type :** isabelle
- **Taille :** 173.0 Ko
- **Modifié :** 2026-08-15 00:15:16
- **Lignes :** 4279
- **Hash MD5 :** `6249ff3841cc`
- **Références sortantes (3) :**
  - ✅ `thy_ref_croisee` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.8)*
  - ❓ `thy_ref_croisee` → `XI` *(l.2947)*
  - ❓ `thy_ref_croisee` → `SpectralMethodCore` *(l.3795)*

### `agent-multiloop-Gabriel-local\theories\methode_spectral_de.thy`
- **Type :** isabelle
- **Taille :** 151.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 3742
- **Hash MD5 :** `e8398038e1a3`
- **Références sortantes (3) :**
  - ✅ `thy_ref_croisee` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.3)*
  - ❓ `thy_ref_croisee` → `XI` *(l.2673)*
  - ❓ `thy_ref_croisee` → `SpectralMethodCore` *(l.3405)*

### `agent-multiloop-Gabriel-local\theories\methode_spectral_en.thy`
- **Type :** isabelle
- **Taille :** 146.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 3740
- **Hash MD5 :** `b8e46fa93b8a`
- **Références sortantes (3) :**
  - ✅ `thy_ref_croisee` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.3)*
  - ❓ `thy_ref_croisee` → `XI` *(l.2670)*
  - ❓ `thy_ref_croisee` → `SpectralMethodCore` *(l.3402)*

### `agent-multiloop-Gabriel-local\theories\methode_spectral_es.thy`
- **Type :** isabelle
- **Taille :** 149.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 3741
- **Hash MD5 :** `c331e4aff5b6`
- **Références sortantes (3) :**
  - ✅ `thy_ref_croisee` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.3)*
  - ❓ `thy_ref_croisee` → `XI` *(l.2671)*
  - ❓ `thy_ref_croisee` → `SpectralMethodCore` *(l.3403)*

### `agent-multiloop-Gabriel-local\theories\methode_spectral_ja.thy`
- **Type :** isabelle
- **Taille :** 153.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 3669
- **Hash MD5 :** `f945e6d3c11d`
- **Références sortantes (3) :**
  - ✅ `thy_ref_croisee` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.3)*
  - ❓ `thy_ref_croisee` → `XI` *(l.2634)*
  - ❓ `thy_ref_croisee` → `SpectralMethodCore` *(l.3350)*

### `agent-multiloop-Gabriel-local\theories\methode_spectral_pt.thy`
- **Type :** isabelle
- **Taille :** 148.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 3741
- **Hash MD5 :** `b1fde81655eb`
- **Références sortantes (3) :**
  - ✅ `thy_ref_croisee` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.3)*
  - ❓ `thy_ref_croisee` → `XI` *(l.2671)*
  - ❓ `thy_ref_croisee` → `SpectralMethodCore` *(l.3403)*

### `agent-multiloop-Gabriel-local\theories\methode_spectral_ru.thy`
- **Type :** isabelle
- **Taille :** 185.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 3747
- **Hash MD5 :** `7e40dcdb37c5`
- **Références sortantes (3) :**
  - ✅ `thy_ref_croisee` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.3)*
  - ❓ `thy_ref_croisee` → `XI` *(l.2672)*
  - ❓ `thy_ref_croisee` → `SpectralMethodCore` *(l.3408)*

### `agent-multiloop-Gabriel-local\theories\methode_spectral_zh.thy`
- **Type :** isabelle
- **Taille :** 141.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 3672
- **Hash MD5 :** `3c9bf741e034`
- **Références sortantes (3) :**
  - ✅ `thy_ref_croisee` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.3)*
  - ❓ `thy_ref_croisee` → `XI` *(l.2628)*
  - ❓ `thy_ref_croisee` → `SpectralMethodCore` *(l.3353)*

### `agent-multiloop-Gabriel-local\theories\projects\config\config_savard_01.yml`
- **Type :** yaml
- **Taille :** 422.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 11
- **Hash MD5 :** `0ef37ad7f8bb`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\config\config_savard_02.yml`
- **Type :** yaml
- **Taille :** 422.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 11
- **Hash MD5 :** `8205ef49a0ef`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\config\config_savard_03.yml`
- **Type :** yaml
- **Taille :** 422.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 11
- **Hash MD5 :** `381c9aaca79a`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\config\config_savard_04.yml`
- **Type :** yaml
- **Taille :** 422.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 11
- **Hash MD5 :** `6afb17f1e4ce`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\config\config_savard_05.yml`
- **Type :** yaml
- **Taille :** 422.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 11
- **Hash MD5 :** `c9f61eb5e39e`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\config\config_savard_06.yml`
- **Type :** yaml
- **Taille :** 422.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 11
- **Hash MD5 :** `e7f810592a5d`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\config\config_savard_07.yml`
- **Type :** yaml
- **Taille :** 422.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 11
- **Hash MD5 :** `d847bb13f855`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\config\config_savard_08.yml`
- **Type :** yaml
- **Taille :** 422.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 11
- **Hash MD5 :** `c1fe7b25af40`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\config\config_savard_09.yml`
- **Type :** yaml
- **Taille :** 422.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 11
- **Hash MD5 :** `df8c56e3b4d0`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\config\config_savard_10.yml`
- **Type :** yaml
- **Taille :** 422.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 11
- **Hash MD5 :** `3714cf83412a`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\dot\graphe_savard_01.dot`
- **Type :** autre
- **Taille :** 501.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 12
- **Hash MD5 :** `ad74dcd3c5bb`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\dot\graphe_savard_02.dot`
- **Type :** autre
- **Taille :** 501.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 12
- **Hash MD5 :** `514ea9763e97`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\dot\graphe_savard_03.dot`
- **Type :** autre
- **Taille :** 501.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 12
- **Hash MD5 :** `05077014f84b`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\dot\graphe_savard_04.dot`
- **Type :** autre
- **Taille :** 501.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 12
- **Hash MD5 :** `d8942cb0a87a`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\dot\graphe_savard_05.dot`
- **Type :** autre
- **Taille :** 501.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 12
- **Hash MD5 :** `26ad402bdf13`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\dot\graphe_savard_06.dot`
- **Type :** autre
- **Taille :** 501.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 12
- **Hash MD5 :** `083206c73bf0`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\dot\graphe_savard_07.dot`
- **Type :** autre
- **Taille :** 501.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 12
- **Hash MD5 :** `69df273b3cef`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\dot\graphe_savard_08.dot`
- **Type :** autre
- **Taille :** 501.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 12
- **Hash MD5 :** `394c4232027a`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\dot\graphe_savard_09.dot`
- **Type :** autre
- **Taille :** 501.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 12
- **Hash MD5 :** `eeaf0e696d2f`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\dot\graphe_savard_10.dot`
- **Type :** autre
- **Taille :** 501.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 12
- **Hash MD5 :** `25bf18486bc0`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot01.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `856949bc31cf`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot02.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `7d3a5af8959a`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot03.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `104401255b32`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot04.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `faa8e4a23246`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot05.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `1d9fdafef195`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot06.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `d09733b0274e`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot07.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `ab1909e3518e`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot08.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `c63ad767e904`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot09.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `0d5d91697418`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot10.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `771e6c3fd08d`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot11.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `79bbc1bfd545`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot12.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `c8977376c5c2`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot13.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `1037c256f2ee`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot14.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `fb49bf028908`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot15.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `f55910ef9b44`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot16.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `0a99adcdb15f`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot17.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `29da5e98eaec`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot18.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `d086c8546195`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot19.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `409a9e8abd3b`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot20.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `fb6e5d88b730`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot21.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `678cba5d0fe3`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot22.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `4e06ef13564e`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot23.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `3baeff0c33e0`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot24.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `092a96e378d3`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\Slot25.lean`
- **Type :** autre
- **Taille :** 538.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `8c7a9537d0eb`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\lakefile.lean`
- **Type :** autre
- **Taille :** 816.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 26
- **Hash MD5 :** `47a92798a489`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\lean\lean-toolchain`
- **Type :** autre
- **Taille :** 26.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 2
- **Hash MD5 :** `4e8d672a4cae`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_01.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `e7c52adebde7`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_02.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `6ee62817ae27`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_03.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `1dce6c842ffd`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_04.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `9c6433bc1890`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_05.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `35773cf77bf2`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_06.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `8df7b183cd27`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_07.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `93e91d3fa09c`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_08.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `7467416ec01c`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_09.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `6a1d75f139e5`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_10.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `31a76c5c7c64`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_11.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `cc9c7bbde5c1`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_12.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `1f60a3e354f3`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_13.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `2cb0111470da`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_14.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `89ef902bd8a8`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_15.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `b2ef6336b101`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_16.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `1bfc72c4efd5`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_17.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `05cd8bd0d2f4`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_18.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `55db4ded44a3`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_19.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `9f1701d84182`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_20.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `28dafc4b3a28`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_21.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `6e0e90b4cff8`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_22.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `53fdf9b9875e`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_23.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `9712bd254737`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_24.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `4d1adba3c77b`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_25.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `2fc548583eed`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_26.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `36521556af69`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_27.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `db3e4014738b`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_28.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `e33cfc9b9403`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_29.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `85f0c1bfa656`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_30.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `1e2d25ea1781`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_31.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `3765c2e2336e`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_32.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `169c8e0906cc`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_33.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `a63606d3cba1`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_34.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `46dbd838c342`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_35.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `cbba14fccc43`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_36.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `6c5a49e35ec7`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_37.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `3ca9c116400f`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_38.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `0ed8f71bdf21`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_39.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `986548d988f5`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_40.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `15e1188de5a0`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_41.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `de90da168c93`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_42.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `4947abd51b9a`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_43.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `0f7104b0e108`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_44.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `5ff3be2759bf`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_45.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `c4a6a309b6a4`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_46.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `304dd5931798`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_47.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `e3c75712396c`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_48.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `b3c4232bf2f4`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_49.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `face7b464c6b`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\md\note_savard_50.md`
- **Type :** markdown
- **Taille :** 448.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `b0be69d1368f`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\notebooks\notebook_savard_01.ipynb`
- **Type :** autre
- **Taille :** 734.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 37
- **Hash MD5 :** `9dec55797c50`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\notebooks\notebook_savard_02.ipynb`
- **Type :** autre
- **Taille :** 734.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 37
- **Hash MD5 :** `29632d2d3955`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\notebooks\notebook_savard_03.ipynb`
- **Type :** autre
- **Taille :** 734.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 37
- **Hash MD5 :** `df2ca73ab8c2`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\notebooks\notebook_savard_04.ipynb`
- **Type :** autre
- **Taille :** 734.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 37
- **Hash MD5 :** `940dad8e0b92`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\notebooks\notebook_savard_05.ipynb`
- **Type :** autre
- **Taille :** 734.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 37
- **Hash MD5 :** `51899aa231c7`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\notebooks\notebook_savard_06.ipynb`
- **Type :** autre
- **Taille :** 734.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 37
- **Hash MD5 :** `91d699555a53`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\notebooks\notebook_savard_07.ipynb`
- **Type :** autre
- **Taille :** 734.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 37
- **Hash MD5 :** `9a37f678ba52`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\notebooks\notebook_savard_08.ipynb`
- **Type :** autre
- **Taille :** 734.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 37
- **Hash MD5 :** `de2dcf712e16`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\notebooks\notebook_savard_09.ipynb`
- **Type :** autre
- **Taille :** 734.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 37
- **Hash MD5 :** `d51311829738`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\notebooks\notebook_savard_10.ipynb`
- **Type :** autre
- **Taille :** 734.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 37
- **Hash MD5 :** `4deda34e53d7`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_01.thy`
- **Type :** isabelle
- **Taille :** 0.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 1
- **Hash MD5 :** `d41d8cd98f00`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_02.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `2ea467077d9b`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_03.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `3c318c9fe142`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_04.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `813108541d06`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_05.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `0792de625835`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_06.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `d025b023d294`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_07.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `b493da1bebf6`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_08.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `dd9f3d9c922c`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_09.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `2bceac621d82`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_10.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `22c67a9a9316`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_100.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `bfe6883f678b`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_11.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `42b0f5d2de4d`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_12.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `b77bc71a80cd`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_13.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `b79e2571233a`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_14.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `76296b43f026`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_15.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `311b0f0025f5`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_16.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `cd9cba324c23`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_17.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `d59290057e41`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_18.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `dcab17f10438`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_19.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `db4ddeeebc4d`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_20.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `334b482c0df9`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_21.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `8085a5acb4c5`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_22.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `91037999fa32`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_23.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `fa1da0f78530`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_24.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `750b231e0064`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_25.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `e33745715ff6`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_26.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `24f69cb5b555`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_27.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `9969f91cc70f`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_28.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `8a37e5cc98b2`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_29.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `888b32ca0e4b`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_30.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `f878b0b01d12`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_31.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `3192bf7dceea`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_32.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `ec8134a4ca63`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_33.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `767dd5e403ec`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_34.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `6e006a466ec3`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_35.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `2719cfb0f816`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_36.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `2e2a06f0831a`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_37.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `eb5cc1988aae`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_38.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `59d32a274a6f`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_39.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `850db88cc3b4`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_40.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `83b075cc462f`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_41.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `6031603251a0`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_42.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `20ee4c0a8d47`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_43.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `640bf5bbb4f1`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_44.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `0fe90e37ccd7`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_45.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `10d2ba1fac8b`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_46.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `444ca0096df1`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_47.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `14311716a4ab`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_48.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `f61f6807e166`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_49.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `5c9569cf3d27`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_50.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `5241c6583417`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_51.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `9d59ca83239b`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_52.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `ee6a24db1442`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_53.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `9f74e4a53443`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_54.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `2adf69607e9c`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_55.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `a83264b541d9`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_56.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `23184b130f4e`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_57.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `d2df6b243f59`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_58.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `1db092615f7a`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_59.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `62758d93cb0f`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_60.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `33683116d5eb`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_61.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `dce0ffdfbf90`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_62.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `33dbfaf6a6cd`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_63.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `7a20a93f0102`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_64.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `e8b657e7fb4a`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_65.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `51e6bf0163a5`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_66.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `c429d02c8e82`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_67.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `1c76ed1a9c9f`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_68.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `6d48a18c41f9`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_69.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `b023203fb864`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_70.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `02ca3432cecf`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_71.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `e782c940cdd9`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_72.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `906682de72c0`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_73.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `27f6689e5c63`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_74.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `edb60e933bd0`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_75.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `55d0fb832d00`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_76.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `c699fe15ae43`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_77.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `cb16dbeaeb91`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_78.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `f38d81f155f0`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_79.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `d916b06d6c00`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_80.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `5094874790ee`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_81.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `2556a71d579e`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_82.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `e888975c758d`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_83.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `8eb1261052cf`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_84.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `6c271a139673`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_85.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `d2b6800823c5`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_86.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `cda46c99f0ee`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_87.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `8d113eb9504c`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_88.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `f63f3b0f1957`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_89.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `0b7cdeceb443`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_90.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `4a303767cbc6`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_91.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `3123a8fc7434`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_92.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `c28c5cda8cd7`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_93.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `991e868f5ea3`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_94.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `83425900c677`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_95.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `27c30856cb42`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_96.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `39f2a02c7d1f`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_97.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `471d3702c886`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_98.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `eb4543c8ea4c`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_99.thy`
- **Type :** isabelle
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `0c5c64815a57`
- **Références sortantes (1) :**
  - ❓ `thy_import` → `Main` *(l.10)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_01.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `84ca45aba9e7`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_02.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `2c5f94c20d2e`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_03.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `1b21466b07b4`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_04.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `a2c9859ecc72`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_05.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `e56114bb0bca`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_06.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `a8b2aaf1ab2c`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_07.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `b7e068b1f0d0`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_08.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `d823a27a7e3b`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_09.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `9795c648570e`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_10.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `17d288aa015e`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_11.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `af8becd76bf6`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_12.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `c29c23e1a374`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_13.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `780c0f96b3ed`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_14.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `64409753b5a9`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_15.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `9e7f0d9ed480`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_16.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `da6cabe70f71`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_17.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `bd4aa39b47b5`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_18.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `672f8c1c1cb6`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_19.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `5c744acfea8a`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_20.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `1b244bd13a9e`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_21.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `90a2444ca738`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_22.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `58964bbfb111`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_23.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `9b4f0265998d`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_24.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `b4010a0c51d7`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\py\analyse_savard_25.py`
- **Type :** python
- **Taille :** 582.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `e4aca8b23f63`
- **Références sortantes (1) :**
  - ❓ `import_module` → `__future__` *(l.9)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_01\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `fbc40c3c6d5f`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_02\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `175a2fa38cf0`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_03\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `71910649c225`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_04\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `e0162c4d837e`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_05\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `ce65951d25d3`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_06\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `56cf696384ff`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_07\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `7b7c176fb18e`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_08\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `1368b61ef04c`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_09\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `37d0f3efe005`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_10\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `167a43295ca8`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_11\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `0809761c6313`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_12\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `74b47d189357`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_13\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `95c4ad67eb9f`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_14\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `f5a461fb16dd`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_15\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `67da3b020b3a`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_16\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `5f5ffc04b9f2`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_17\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `dc42f5fac538`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_18\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `ea921f89c7b4`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_19\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `0b328a0f4b8b`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_20\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `fc61f5cdebd4`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_21\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `54cf36909be6`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_22\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `6f075243e04c`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_23\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `3a18bd0784ba`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_24\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `b255de4c9adf`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\roots\session_25\ROOT`
- **Type :** autre
- **Taille :** 934.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 25
- **Hash MD5 :** `4f2a17ef070f`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\scripts\script_savard_01.sh`
- **Type :** shell
- **Taille :** 424.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 11
- **Hash MD5 :** `bca310f5bd21`
- **Références sortantes (1) :**
  - ❓ `shell_appel` → `A` *(l.4)*

### `agent-multiloop-Gabriel-local\theories\projects\scripts\script_savard_02.sh`
- **Type :** shell
- **Taille :** 424.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 11
- **Hash MD5 :** `8ab6db56f1ba`
- **Références sortantes (1) :**
  - ❓ `shell_appel` → `A` *(l.4)*

### `agent-multiloop-Gabriel-local\theories\projects\scripts\script_savard_03.sh`
- **Type :** shell
- **Taille :** 424.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 11
- **Hash MD5 :** `0728c58fbfa5`
- **Références sortantes (1) :**
  - ❓ `shell_appel` → `A` *(l.4)*

### `agent-multiloop-Gabriel-local\theories\projects\scripts\script_savard_04.sh`
- **Type :** shell
- **Taille :** 424.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 11
- **Hash MD5 :** `59a2a2068edc`
- **Références sortantes (1) :**
  - ❓ `shell_appel` → `A` *(l.4)*

### `agent-multiloop-Gabriel-local\theories\projects\scripts\script_savard_05.sh`
- **Type :** shell
- **Taille :** 424.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 11
- **Hash MD5 :** `41db1fefbbc4`
- **Références sortantes (1) :**
  - ❓ `shell_appel` → `A` *(l.4)*

### `agent-multiloop-Gabriel-local\theories\projects\scripts\script_savard_06.sh`
- **Type :** shell
- **Taille :** 424.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 11
- **Hash MD5 :** `1f240148638a`
- **Références sortantes (1) :**
  - ❓ `shell_appel` → `A` *(l.4)*

### `agent-multiloop-Gabriel-local\theories\projects\scripts\script_savard_07.sh`
- **Type :** shell
- **Taille :** 424.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 11
- **Hash MD5 :** `ae690cc5bb5d`
- **Références sortantes (1) :**
  - ❓ `shell_appel` → `A` *(l.4)*

### `agent-multiloop-Gabriel-local\theories\projects\scripts\script_savard_08.sh`
- **Type :** shell
- **Taille :** 424.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 11
- **Hash MD5 :** `0977a6920a81`
- **Références sortantes (1) :**
  - ❓ `shell_appel` → `A` *(l.4)*

### `agent-multiloop-Gabriel-local\theories\projects\scripts\script_savard_09.sh`
- **Type :** shell
- **Taille :** 424.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 11
- **Hash MD5 :** `a36832f895cb`
- **Références sortantes (1) :**
  - ❓ `shell_appel` → `A` *(l.4)*

### `agent-multiloop-Gabriel-local\theories\projects\scripts\script_savard_10.sh`
- **Type :** shell
- **Taille :** 424.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 11
- **Hash MD5 :** `399f3120c1b4`
- **Références sortantes (1) :**
  - ❓ `shell_appel` → `A` *(l.4)*

### `agent-multiloop-Gabriel-local\theories\projects\svg\schema_savard_01.svg`
- **Type :** autre
- **Taille :** 636.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Hash MD5 :** `9a1d24dfd20d`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\svg\schema_savard_02.svg`
- **Type :** autre
- **Taille :** 636.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Hash MD5 :** `e36e9c303be7`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\svg\schema_savard_03.svg`
- **Type :** autre
- **Taille :** 636.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Hash MD5 :** `2d77c4f2c681`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\svg\schema_savard_04.svg`
- **Type :** autre
- **Taille :** 636.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Hash MD5 :** `051c26ee54ca`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\svg\schema_savard_05.svg`
- **Type :** autre
- **Taille :** 636.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Hash MD5 :** `353f3429f0ec`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\svg\schema_savard_06.svg`
- **Type :** autre
- **Taille :** 636.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Hash MD5 :** `a89da8581436`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\svg\schema_savard_07.svg`
- **Type :** autre
- **Taille :** 636.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Hash MD5 :** `02ed0c734146`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\svg\schema_savard_08.svg`
- **Type :** autre
- **Taille :** 636.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Hash MD5 :** `fb8b9ba00156`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\svg\schema_savard_09.svg`
- **Type :** autre
- **Taille :** 636.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Hash MD5 :** `1a251d5cedce`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\svg\schema_savard_10.svg`
- **Type :** autre
- **Taille :** 636.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Hash MD5 :** `fb6ec77fee35`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\biblio_savard_01.bib`
- **Type :** latex
- **Taille :** 441.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 13
- **Hash MD5 :** `7beed595b4ec`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\biblio_savard_02.bib`
- **Type :** latex
- **Taille :** 441.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 13
- **Hash MD5 :** `073ff66e07af`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\biblio_savard_03.bib`
- **Type :** latex
- **Taille :** 441.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 13
- **Hash MD5 :** `e50498e4aad7`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\biblio_savard_04.bib`
- **Type :** latex
- **Taille :** 441.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 13
- **Hash MD5 :** `bbcfb4e1a3a0`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\biblio_savard_05.bib`
- **Type :** latex
- **Taille :** 441.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 13
- **Hash MD5 :** `364123bb62c8`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\biblio_savard_06.bib`
- **Type :** latex
- **Taille :** 441.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 13
- **Hash MD5 :** `3913046b87a1`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\biblio_savard_07.bib`
- **Type :** latex
- **Taille :** 441.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 13
- **Hash MD5 :** `60c15a9b8d8b`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\biblio_savard_08.bib`
- **Type :** latex
- **Taille :** 441.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 13
- **Hash MD5 :** `b8871fb1b419`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\biblio_savard_09.bib`
- **Type :** latex
- **Taille :** 441.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 13
- **Hash MD5 :** `66c808675f8b`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\biblio_savard_10.bib`
- **Type :** latex
- **Taille :** 441.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 13
- **Hash MD5 :** `f77f204aa434`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_01.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `dcb641fe3930`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_02.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `b7a9bbb00ee0`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_03.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `9fdacd945f51`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_04.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `0aebe862b318`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_05.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `801f76ec2429`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_06.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `1ba4d77e0f67`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_07.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `afb4c29b9e68`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_08.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `5af3e257fc05`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_09.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `2bd0827e69b2`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_10.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `82b30a438f8b`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_100.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `934bdb4acd0a`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_11.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `96e75cdfd98c`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_12.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `91528c22706b`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_13.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `b944cc728d29`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_14.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `d88a9f417ba5`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_15.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `d23fd56107d1`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_16.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `c071c17021a0`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_17.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `b8e32428756b`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_18.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `772783ccbf98`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_19.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `8caddf7b1148`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_20.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `e06389173b72`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_21.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `d7321bb7d2ca`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_22.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `d6c80710dfa8`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_23.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `69f4e484694e`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_24.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `0817f13e4582`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_25.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `3ea07f342651`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_26.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `a4538103a3f3`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_27.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `21b213cb4ca0`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_28.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `cc0420070dd9`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_29.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `081a2bcb8a28`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_30.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `3dace3f29bf7`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_31.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `1b5d5e4d2094`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_32.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `74b30b710a12`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_33.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `a5a8fa48e200`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_34.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `54f2012daee2`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_35.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `0e8a3ad91bd2`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_36.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `65e1e1f3c7fc`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_37.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `cce971013db2`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_38.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `6c6c1111506c`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_39.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `02e0fb295970`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_40.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `e16811647310`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_41.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `d48dd09604c2`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_42.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `5b1a2459b7de`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_43.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `53044ad2ae81`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_44.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `95c67312bed3`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_45.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `55c3b47da168`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_46.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `c1316a273589`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_47.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `2ff86279c308`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_48.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `955f001f93f9`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_49.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `ea6e84d9d2ac`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_50.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `558cd25c618d`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_51.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `82fd59d40819`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_52.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `9cf306e32fd5`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_53.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `ef9955e4fb2c`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_54.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `2ab9a83f0747`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_55.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `cbfe87c00da2`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_56.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `69598757b4f8`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_57.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `263041f875ee`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_58.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `ecedc77a8268`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_59.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `b69e01bc143c`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_60.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `0466b0953328`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_61.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `e6436d1f780d`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_62.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `aba94dda98c5`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_63.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `ce754317e28a`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_64.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `015888868862`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_65.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `2fd177889cc1`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_66.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `68128ecaaa25`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_67.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `da966a902859`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_68.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `18315e77086d`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_69.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `91cff3266c9b`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_70.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `132c9dafcd8a`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_71.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `4cec3559c274`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_72.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `0f0b36b4c70e`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_73.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `4e617f39cfad`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_74.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `2e381c56a5a5`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_75.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `597a0bbba415`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_76.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `92b52c618c8d`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_77.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `f314bdef6c7a`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_78.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `abd14c3d83e7`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_79.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `dc5340da8f12`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_80.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `e6d08cd72804`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_81.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `21d42f03bb1e`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_82.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `4a8180650cee`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_83.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `fe98b1c8add8`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_84.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `2c0e0b63ab5b`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_85.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `14951e51d7f3`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_86.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `daa47c670109`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_87.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `1519cc2543a5`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_88.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `3009ef9f8823`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_89.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `e13b49fcd249`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_90.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `1e87160dca71`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_91.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `c3b3785a90bc`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_92.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `143ace178dbd`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_93.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `136c1fbd9ea1`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_94.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `b9fdb9984981`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_95.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `b6617ae0b852`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_96.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `a2c76886e100`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_97.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `4e598ae95cb7`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_98.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `5f389bc57191`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\tex\projet_uni_car_savard_99.tex`
- **Type :** latex
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `fbc56c35ab96`
- **Références sortantes (5) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.7)*
  - ❓ `latex_inclusion` → `babel` *(l.8)*
  - ❓ `latex_inclusion` → `amsmath` *(l.9)*
  - ❓ `latex_inclusion` → `amssymb` *(l.10)*
  - ❓ `latex_inclusion` → `geometry` *(l.11)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\Géométrie du Spectre des Nombres Premiers — Brouillon Conceptuel Savard 2026.pdf`
- **Type :** autre
- **Taille :** 329.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Hash MD5 :** `c34157b057d3`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_01.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `bde078e1bf3e`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_02.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `23f6d09b338a`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_03.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `a6964fe1876b`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_04.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `34856f7f0651`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_05.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `029536b81679`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_06.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `1fd4ab467f2c`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_07.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `4ceb39a20e59`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_08.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `ba453af84f82`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_09.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `391cc3bed6b1`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_10.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `742d29c806e3`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_100.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `7d76c9635819`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_11.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `b713db1995ad`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_12.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `b9025afc2e2a`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_13.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `7c95dfaeec00`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_14.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `19e8d2fdb22a`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_15.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `e5dea5bbe8d8`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_16.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `fdb98454499f`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_17.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `e085d8d2f32a`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_18.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `3953eabe520c`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_19.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `4c60b7c0de41`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_20.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `f7305953d413`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_21.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `a4c9e9392628`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_22.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `f246ee9fb8e9`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_23.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `e6b251542ae9`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_24.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `c0c12a28cd28`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_25.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `2a8cbfd0c8b8`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_26.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `07bbf6ecda49`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_27.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `0436c78a8d27`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_28.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `a0cb3cac5bc2`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_29.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `9020196187b3`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_30.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `1e952964a9a3`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_31.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `48e8a9f9be89`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_32.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `6dde85382f5c`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_33.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `decedea2b3d4`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_34.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `cffc9ff58976`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_35.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `d204c8586b10`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_36.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `b78c39392585`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_37.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `e51b4368d5a3`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_38.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `eed360fb9d0c`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_39.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `946000ddfcc8`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_40.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `60121ca61cf3`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_41.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `beeb14bbe99f`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_42.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `40d80697b198`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_43.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `8f3974ac787e`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_44.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `aa2a829ce515`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_45.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `a653f9d6505e`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_46.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `ccfbeb86f4df`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_47.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `6808da63d62f`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_48.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `d4c72e04dbb2`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_49.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `ade9e0f18a72`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_50.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `c922e02e6a8d`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_51.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `a0509feb9854`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_52.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `d246c592b05c`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_53.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `14b13c83ec6b`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_54.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `b0e3ee884cfa`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_55.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `97411357d095`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_56.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `3c7def933665`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_57.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `779ef3879c1f`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_58.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `a64cc90ab757`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_59.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `0e39d5b0c248`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_60.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `35c646428ef7`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_61.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `e1fd3666d5a0`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_62.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `1e49646f7ecb`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_63.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `bd9e675ccd72`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_64.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `4ee39a657d6c`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_65.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `11651802bc14`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_66.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `627671427f41`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_67.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `8b713cea2101`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_68.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `4945145fbcf4`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_69.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `e6aea8b9184f`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_70.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `2958b4228b3b`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_71.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `0f6b0619a08f`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_72.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `af7b0ac78371`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_73.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `32ad64bd43f2`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_74.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `02e54c7897c8`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_75.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `3c94f97653f6`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_76.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `f655cb407d04`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_77.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `ed5d3a9ce14c`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_78.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `84f50b4b48c5`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_79.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `09e93afc51bf`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_80.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `0373813d857a`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_81.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `7de1a13126da`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_82.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `f249d5bb3ba4`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_83.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `3d6b10d03b53`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_84.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `daf28269b6e9`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_85.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `345917605647`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_86.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `5cf5cc95c87a`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_87.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `f08f7dc2ed7b`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_88.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `ce093694677f`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_89.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `429d1fc1dabe`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_90.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `6c3f6b085820`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_91.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `3eb94b88901e`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_92.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `30b8e450b91a`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_93.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `6733f896cecd`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_94.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `cfea26815f54`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_95.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `58accd661a94`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_96.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `889777bec8c7`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_97.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `ea47d09d1351`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_98.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `1dac11a7f5f6`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\projects\txt\projet_uni_car_savard_99.txt`
- **Type :** texte
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 31
- **Hash MD5 :** `866e9cb52844`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.log`
- **Type :** autre
- **Taille :** 59.4 Ko
- **Modifié :** 2026-08-13 00:02:57
- **Lignes :** 1668
- **Hash MD5 :** `dc04c64da9f6`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.pdf`
- **Type :** autre
- **Taille :** 519.9 Ko
- **Modifié :** 2026-08-13 00:02:57
- **Hash MD5 :** `17bbea50ca7c`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\Geometrie_du_Spectre_des_Nombres_Premiers_2026.tex`
- **Type :** latex
- **Taille :** 79.4 Ko
- **Modifié :** 2026-08-15 00:15:16
- **Lignes :** 1459
- **Hash MD5 :** `7fe724633c0d`
- **Références sortantes (24) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.2)*
  - ❓ `latex_inclusion` → `fontenc` *(l.3)*
  - ❓ `latex_inclusion` → `babel` *(l.4)*
  - ❓ `latex_inclusion` → `lmodern` *(l.5)*
  - ❓ `latex_inclusion` → `amsmath` *(l.6)*
  - ❓ `latex_inclusion` → `amssymb` *(l.7)*
  - ❓ `latex_inclusion` → `xcolor` *(l.8)*
  - ❓ `latex_inclusion` → `geometry` *(l.9)*
  - ❓ `latex_inclusion` → `hyperref` *(l.10)*
  - ❓ `latex_inclusion` → `longtable` *(l.11)*
  - ❓ `latex_inclusion` → `array` *(l.12)*
  - ❓ `latex_inclusion` → `booktabs` *(l.13)*
  - ❓ `latex_inclusion` → `enumitem` *(l.14)*
  - ❓ `latex_inclusion` → `titlesec` *(l.15)*
  - ❓ `latex_inclusion` → `tocloft` *(l.16)*
  - ❓ `latex_inclusion` → `setspace` *(l.17)*
  - ❓ `latex_inclusion` → `microtype` *(l.18)*
  - ❓ `latex_inclusion` → `etoolbox` *(l.19)*
  - ❓ `latex_inclusion` → `fancyhdr` *(l.20)*
  - ❓ `latex_inclusion` → `xurl` *(l.21)*
  - ❓ `latex_inclusion` → `underscore` *(l.22)*
  - ❓ `latex_inclusion` → `listings` *(l.23)*
  - ❓ `latex_inclusion` → `tcolorbox` *(l.24)*
  - ❓ `latex_inclusion` → `newunicodechar` *(l.25)*

### `agent-multiloop-Gabriel-local\theories\tex\PDF\Geometrie_du_Spectre_des_Nombres_Premiers.pdf`
- **Type :** autre
- **Taille :** 456.9 Ko
- **Modifié :** 2026-08-08 12:31:47
- **Hash MD5 :** `34dde3987edb`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\PDF\README_pdf.txt`
- **Type :** texte
- **Taille :** 8.3 Ko
- **Modifié :** 2026-08-09 21:24:31
- **Lignes :** 167
- **Hash MD5 :** `124f7ebf07bb`
- **Références sortantes (4) :**
  - ❓ `ref_generique` → `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local.git` *(l.149)*
  - ❓ `ref_generique` → `//github.com/2racinede4carreunivers-dev/Theorie-mathematique-philippe-thomas-savard-2026.git` *(l.150)*
  - ❓ `ref_generique` → `//github.com/2racinede4carreunivers-dev/Ia_geo_spec_prem_app_deplo.git` *(l.151)*
  - ❓ `ref_generique` → `//www.universestaucarre.com` *(l.152)*

### `agent-multiloop-Gabriel-local\theories\tex\README_pdf.md`
- **Type :** markdown
- **Taille :** 7.8 Ko
- **Modifié :** 2026-08-15 00:15:16
- **Lignes :** 152
- **Hash MD5 :** `a503aeb9b006`
- **Références sortantes (2) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.147)*
  - ✅ `ref_generique` → `README.md` *(l.148)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.aux`
- **Type :** autre
- **Taille :** 11.2 Ko
- **Modifié :** 2026-08-07 19:52:03
- **Lignes :** 173
- **Hash MD5 :** `5a18bbde30ba`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.aux`
- **Type :** autre
- **Taille :** 11.2 Ko
- **Modifié :** 2026-08-07 08:09:36
- **Lignes :** 173
- **Hash MD5 :** `2b4449cee8ed`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.listing`
- **Type :** autre
- **Taille :** 1.5 Ko
- **Modifié :** 2026-08-07 08:09:36
- **Lignes :** 39
- **Hash MD5 :** `ab594b247975`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.log`
- **Type :** autre
- **Taille :** 61.5 Ko
- **Modifié :** 2026-08-07 08:09:36
- **Lignes :** 1737
- **Hash MD5 :** `49002a6b94db`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.out`
- **Type :** autre
- **Taille :** 13.4 Ko
- **Modifié :** 2026-08-07 08:09:36
- **Lignes :** 46
- **Hash MD5 :** `a0d03ef2b623`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.pdf`
- **Type :** autre
- **Taille :** 579.3 Ko
- **Modifié :** 2026-08-07 08:09:36
- **Hash MD5 :** `a1cf74ccc5f9`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.tex`
- **Type :** latex
- **Taille :** 75.9 Ko
- **Modifié :** 2026-08-07 07:31:40
- **Lignes :** 1413
- **Hash MD5 :** `4ded74694011`
- **Références sortantes (24) :**
  - ❓ `latex_inclusion` → `inputenc` *(l.2)*
  - ❓ `latex_inclusion` → `fontenc` *(l.3)*
  - ❓ `latex_inclusion` → `babel` *(l.4)*
  - ❓ `latex_inclusion` → `lmodern` *(l.5)*
  - ❓ `latex_inclusion` → `amsmath` *(l.6)*
  - ❓ `latex_inclusion` → `amssymb` *(l.7)*
  - ❓ `latex_inclusion` → `xcolor` *(l.8)*
  - ❓ `latex_inclusion` → `geometry` *(l.9)*
  - ❓ `latex_inclusion` → `hyperref` *(l.10)*
  - ❓ `latex_inclusion` → `longtable` *(l.11)*
  - ❓ `latex_inclusion` → `array` *(l.12)*
  - ❓ `latex_inclusion` → `booktabs` *(l.13)*
  - ❓ `latex_inclusion` → `enumitem` *(l.14)*
  - ❓ `latex_inclusion` → `titlesec` *(l.15)*
  - ❓ `latex_inclusion` → `tocloft` *(l.16)*
  - ❓ `latex_inclusion` → `setspace` *(l.17)*
  - ❓ `latex_inclusion` → `microtype` *(l.18)*
  - ❓ `latex_inclusion` → `etoolbox` *(l.19)*
  - ❓ `latex_inclusion` → `fancyhdr` *(l.20)*
  - ❓ `latex_inclusion` → `xurl` *(l.21)*
  - ❓ `latex_inclusion` → `underscore` *(l.22)*
  - ❓ `latex_inclusion` → `listings` *(l.23)*
  - ❓ `latex_inclusion` → `tcolorbox` *(l.24)*
  - ❓ `latex_inclusion` → `newunicodechar` *(l.25)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.corrected.toc`
- **Type :** autre
- **Taille :** 6.0 Ko
- **Modifié :** 2026-08-07 08:09:36
- **Lignes :** 56
- **Hash MD5 :** `e864678074b9`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.listing`
- **Type :** autre
- **Taille :** 1.5 Ko
- **Modifié :** 2026-08-07 19:52:03
- **Lignes :** 39
- **Hash MD5 :** `ab594b247975`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.log`
- **Type :** autre
- **Taille :** 59.6 Ko
- **Modifié :** 2026-08-07 19:52:04
- **Lignes :** 1659
- **Hash MD5 :** `79a392fa662d`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.out`
- **Type :** autre
- **Taille :** 13.4 Ko
- **Modifié :** 2026-08-07 19:52:03
- **Lignes :** 46
- **Hash MD5 :** `a0d03ef2b623`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.pdf`
- **Type :** autre
- **Taille :** 447.0 Ko
- **Modifié :** 2026-08-06 15:50:42
- **Hash MD5 :** `21d065e089f6`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.quality_report.json`
- **Type :** json
- **Taille :** 213.1 Ko
- **Modifié :** 2026-08-07 18:22:39
- **Lignes :** 4026
- **Hash MD5 :** `88533b75b904`
- **Références sortantes (29) :**
  - ❓ `json_chemin` → ` Copilot — Microsoft E1 — emergent.sh Gordon — Docker Desktop Claude API — Anthropic Gemini — Google Ces co-auteurs ont contribué à la formalisation Isabelle/HOL, à la rédaction assistée, à la vérification des preuves , chacun à part égale avec l'auteur principal.` *(l.17)*
  - ❓ `json_chemin` → ` Copilot — Microsoft E1 — émergent.sh Gordon — Docker Desktop Claude API — Anthropic Gemini — Google Ces co-auteurs ont contribué à la formalisation Isabelle/HOL, à la rédaction assistée, à la vérification des preuves , chacun à part égale avec l'auteur principal.` *(l.18)*
  - ❓ `json_chemin` → `Note liminaire \\\\ Ce document contient des formules, des preuves formelles validées par Isabelle/HOL, et la voix de l'auteur, qui cherche à faire toucher au lecteur ce que la géométrie des nombres premiers lui a fait ressentir. Cette géométrie est la chair qui le touche et qu'il touche en retour. Toute est tiré des documents sources et du fichier methode spectrale. Vous êtes invités a consulter les fichiers Readme des dépôts publics mise en place et à la dispositon des contributeur via PR, de partager, consulter, cloner, selon les permissions de la LICENSE Apach 2.0 Bienvenu a tous.\\_spectral.thy validé par l'assistant de preuve. Méthode Spectrale de Philippe Thomas Savard.` *(l.57)*
  - ❓ `json_chemin` → `Note liminaire \\\\ Ce document contient des formules, des preuves formelles validées par Isabelle/HOL, et la voix de l'auteur, qui cherche à faire toucher au lecteur ce que la géométrie des nombres premiers lui a fait ressentir. Cette géométrie est la chair qui le touche et qu'il touche en retour. Tout est tiré des documents sources et du fichier méthode spectrale. Vous êtes invités à consulter les fichiers README des dépôts publics mise à disposition des contributeurs via PR, de partager, consulter, cloner, selon les permissions de la LICENSE Apache 2.0 Bienvenue à tous.\\_spectral.thy validé par l'assistant de preuve. Méthode Spectrale de Philippe Thomas Savard.` *(l.58)*
  - ❓ `json_chemin` → `Le code Isabelle/HOL correspondant, tiré du fichier methode\\_spectral.thy (Section XII, lignes 365–382), est le suivant :` *(l.287)*
  - ❓ `json_chemin` → `Le code Isabelle/HOL correspondant, tiré du fichier méthode\\_spectral.thy (Section XII, lignes 365–382), est le suivant :` *(l.288)*
  - ❓ `json_chemin` → `Valeurs de référence \\\\ Pour n = 10 : SA(10) = 1 662 et SB(10) = 3 262. Pour n = 11 : SA(11) = 3 326 et SB(11) = 6 590. Ces valeurs sont prouvées formellement par les lemmes SA\\_10, SA\\_11, SB\\_10, SB\\_11 dans le fichier methode\\_spectral.thy.` *(l.377)*
  - ❓ `json_chemin` → `Valeurs de référence \\\\ Pour n = 10 : SA(10) = 1 662 et SB(10) = 3 262. Pour n = 11 : SA(11) = 3 326 et SB(11) = 6 590. Ces valeurs sont prouvées formellement par les femmes SA\\_10, SA\\_11, SB\\_10, SB\\_11 dans le fichier méthode\\_spectral.thy.` *(l.378)*
  - ❓ `json_chemin` → `Ces cinq résultats sont prouvés formellement par les lemmes SA\\_9 à SA\\_13, SB\\_9 à SB\\_13, et digamma\\_calc\\_23 à digamma\\_calc\\_41 dans le fichier methode\\_spectral.thy. Chaque preuve HOL constitue une certification machinique de l'exactitude du calcul.` *(l.627)*
  - ❓ `json_chemin` → `Ces cinq résultats sont prouvés formellement par les femmes SA\\_9 à SA\\_13, SB\\_9 à SB\\_13, et digamma\\_calc\\_23 à digamma\\_calc\\_41 dans le fichier méthode\\_spectral.thy. Chaque preuve HOL constitue une certification machiniste de l'exactitude du calcul.` *(l.628)*
  - ❓ `json_chemin` → `(* Extraits de methode_spectral.thy, section I.5 *)` *(l.637)*
  - ❓ `json_chemin` → `(* Extraits de méthode_spectral.thy, section I.5 *)` *(l.638)*
  - ❓ `json_chemin` → `(* Schema de preuve utilise dans methode_spectral.thy *)` *(l.727)*
  - ❓ `json_chemin` → `(* Schema de preuve utilise dans méthode_spectral.thy *)` *(l.728)*
  - ❓ `json_chemin` → `« La Méthode Spectrale caractérise EXACTEMENT l'ensemble ℙ des nombres premiers — ni plus, ni moins — dans ses trois domaines d'application. » \\\\ — Synthèse formelle, fichier methode\\_spectral.thy, juillet 2026` *(l.787)*
  - ❓ `json_chemin` → `« La Méthode Spectrale caractérise EXACTEMENT l'ensemble ℙ des nombres premiers — ni plus, ni moins — dans ses trois domaines d'application. » \\\\ — Synthèse formelle, fichier méthode\\_spectral.thy, juillet 2026` *(l.788)*
  - ❓ `json_chemin` → `Le théorème de synthèse est le point culminant du fichier methode\\_spectral.thy (version 3.42). Il constitue un ensemble à lui seul : il agrège les cinq faits indépendamment démontrés dans ce fichier en un seul énoncé unifié.` *(l.847)*
  - ❓ `json_chemin` → `Le théorème de synthèse est le point culminant du fichier méthode\\_spectral.thy (version 3.42). Il constitue un ensemble à lui seul : il agrège les cinq faits indépendamment démontrés dans ce fichier en un seul énoncé unifié.` *(l.848)*
  - ❓ `json_chemin` → `Chacun de ces faits est déjà un théorème ou un lemme HOL prouvé dans les sections précédentes du fichier methode\\_spectral.thy. Le théorème de synthèse se contente de les assembler — il n'introduit aucun axiome nouveau.` *(l.857)*
  - ❓ `json_chemin` → `Chacun de ces faits est déjà un théorème ou un femme HOL prouvé dans les sections précédentes du fichier méthode\\_spectral.thy. Le théorème de synthèse se contente de les assembler — il n'introduit aucun axiome nouveau.` *(l.858)*
  - ❓ `json_chemin` → `(* Pour F1 et F3 : voir les lemmes du Pont Savard (Section XIII) dans methode_spectral.thy *)` *(l.877)*
  - ❓ `json_chemin` → `(* Pour F1 et F3 : voir les femmes du Pont Savard (Section XIII) dans méthode_spectral.thy *)` *(l.878)*
  - ❓ `json_chemin` → `Fait & Énoncé & Source dans methode\\_spectral.thy` *(l.887)*
  - ❓ `json_chemin` → `Fait & Énoncé & Source dans méthode\\_spectral.thy` *(l.888)*
  - ❓ `json_chemin` → `Le tableau suivant constitue un index de navigation vers les six postulats fondamentaux et leurs réalisations formelles dans methode\\_spectral.thy :` *(l.1127)*
  - ❓ `json_chemin` → `Le tableau suivant constitue un index de navigation vers les six postulats fondamentaux et leurs réalisations formelles dans méthode\\_spectral.thy :` *(l.1128)*
  - ❓ `json_chemin` → `Copyright 2026 Philippe Thomas Savard \\\\ Le fichier methode\\_spectral.thy et le présent document sont distribués sous les termes de la Licence Apache, Version 2.0 (la « Licence »). Vous ne pouvez utiliser ce fichier qu'en conformité avec la Licence. \\\\ Vous pouvez obtenir une copie de la Licence à l'adresse : \\\\ http://www.apache.org/licenses/LICENSE-2.0 \\\\ Sauf si requis par la loi applicable ou convenu par écrit, le logiciel distribué sous la Licence est distribué « EN L'ÉTAT », SANS GARANTIES NI CONDITIONS D'AUCUNE SORTE, expresses ou implicites. Voir la Licence pour les dispositions spécifiques régissant les autorisations et limitations en vertu de la Licence. \\\\ Dépôt public : https://github.com/PhilippeThomasSavard/Agent-multiloop-Gabriel` *(l.1197)*
  - ❓ `json_chemin` → `Copyright 2026 Philippe Thomas Savard \\\\ Le fichier méthode\\_spectral.thy et le présent document sont distribués sous les termes de la Licence Apache, Version 2.0 (la « Licence »). Vous ne pouvez utiliser ce fichier qu'en conformité avec la Licence. \\\\ Vous pouvez obtenir une copie de la Licence à l'adresse : \\\\ hâte://www.apache.org/licences/LICENSE-2.0 \\\\ Sauf si requis par la loi applicable ou convenu par écrit, le logiciel distribué sous la Licence est distribué « EN L'ÉTAT », SANS GARANTIES NI CONDITIONS D'AUCUNE SORTE, expresses ou implicites. Voir la Licence pour les dispositions spécifiques régissant les autorisations et limitations en vertu de la Licence. \\\\ Dépôt public : hôtes://github.com/PhilippeThomasSavard/Agent-multiloop-Gabriel` *(l.1198)*
  - ✅ `json_chemin` → `agent-multiloop-Gabriel-local\scripts\tex_healthcheck.py` *(l.4019)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.second_pass.quality_report.json`
- **Type :** json
- **Taille :** 272.1 Ko
- **Modifié :** 2026-08-07 07:20:23
- **Lignes :** 4897
- **Hash MD5 :** `9c55c7fa6aa3`
- **Références sortantes (28) :**
  - ❓ `json_chemin` → ` Copilot — Microsoft E1 — emergent.sh Gordon — Docker Desktop Claude API — Anthropic Gemini — Google Ces co-auteurs ont contribué à la formalisation Isabelle/HOL, à la rédaction assistée, à la vérification des preuves , chacun à part égale avec l'auteur principal.` *(l.57)*
  - ❓ `json_chemin` → ` Copilote — Microsoft E1 — émergent.sh Cordon — Docker Desktop Claude API — Anthropic Gamin — Gorge Ces co-auteurs ont contribué à la formalisation Isabelle/HOL, à la rédaction assistée, à la vérification des preuves , chacun à part égale avec l'auteur principal.` *(l.58)*
  - ❓ `json_chemin` → `Note liminaire \\\\ Ce document contient des formules, des preuves formelles validées par Isabelle/HOL, et la voix de l'auteur, qui cherche à faire toucher au lecteur ce que la géométrie des nombres premiers lui a fait ressentir. Cette géométrie est la chair qui le touche et qu'il touche en retour. Toute est tiré des documents sources et du fichier methode. Vous êtes invités a consulter les fichiers Readme des dépôts publics mise en place et à la dispositon des contributeur via PR, de partager, consulter, cloner, selon les permissions de la LICENSE Apach 2.0 Bienvenu a tous.\\_spectral.thy validé par l'assistant de preuve. Méthode Spectrale de Philippe Thomas Savard.` *(l.107)*
  - ❓ `json_chemin` → `Note liminaire \\\\ Ce document contient des formules, des preuves formelles validées par Isabelle/HOL, et la voix de l'auteur, qui cherche à faire toucher au lecteur ce que la géométrie des nombres premiers lui a fait ressentir. Cette géométrie est la chair qui le touche et qu'il touche en retour. Tout est tiré des documents sources et du fichier méthode. Vous êtes invités à consulter les fichiers README des dépôts publics mise à disposition des contributeurs via PR, de partager, consulter, cloner, selon les permissions de la LICENSE Apache 2.0 Bienvenue à tous.\\_spectral.thy validé par l'assistant de preuve. Méthode Spectrale de Philippe Thorax Bavard.` *(l.108)*
  - ❓ `json_chemin` → `Le code Isabelle/HOL correspondant, tiré du fichier methode\\_spectral.thy (Section XII, lignes 365–382), est le suivant :` *(l.377)*
  - ❓ `json_chemin` → `Le code Isabelle/HOL correspondant, tiré du fichier méthode\\_spectral.thy (Section XII, lignes 365–382), est le suivant :` *(l.378)*
  - ❓ `json_chemin` → `Valeurs de référence \\\\ Pour n = 10 : SA(10) = 1 662 et SB(10) = 3 262. Pour n = 11 : SA(11) = 3 326 et SB(11) = 6 590. Ces valeurs sont prouvées formellement par les lemmes SA\\_10, SA\\_11, SB\\_10, SB\\_11 dans le fichier methode\\_spectral.thy.` *(l.467)*
  - ❓ `json_chemin` → `Valeurs de référence \\\\ Pour n = 10 : SA(10) = 1 662 et SB(10) = 3 262. Pour n = 11 : SA(11) = 3 326 et SB(11) = 6 590. Ces valeurs sont prouvées formellement par les femmes SA\\_10, SA\\_11, SB\\_10, SB\\_11 dans le fichier méthode\\_spectral.thy.` *(l.468)*
  - ❓ `json_chemin` → `Ces cinq résultats sont prouvés formellement par les lemmes SA\\_9 à SA\\_13, SB\\_9 à SB\\_13, et digamma\\_calc\\_23 à digamma\\_calc\\_41 dans le fichier methode\\_spectral.thy. Chaque preuve HOL constitue une certification machinique de l'exactitude du calcul.` *(l.727)*
  - ❓ `json_chemin` → `Ces cinq résultats sont prouvés formellement par les femmes SA\\_9 à SA\\_13, SB\\_9 à SB\\_13, et digamma\\_calc\\_23 à digamma\\_calc\\_41 dans le fichier méthode\\_spectral.thy. Chaque preuve HOL constitue une certification machiniste de l'exactitude du calcul.` *(l.728)*
  - ❓ `json_chemin` → `(* Extraits de methode_spectral.thy, section I.5 *)` *(l.737)*
  - ❓ `json_chemin` → `(* Extraits de méthode_spectral.thy, section I.5 *)` *(l.738)*
  - ❓ `json_chemin` → `(* Schema de preuve utilise dans methode_spectral.thy *)` *(l.827)*
  - ❓ `json_chemin` → `(* Schéma de preuve utilise dans méthode_spectral.thy *)` *(l.828)*
  - ❓ `json_chemin` → `« La Méthode Spectrale caractérise EXACTEMENT l'ensemble ℙ des nombres premiers — ni plus, ni moins — dans ses trois domaines d'application. » \\\\ — Synthèse formelle, fichier methode\\_spectral.thy, juillet 2026` *(l.897)*
  - ❓ `json_chemin` → `« La Méthode Spectrale caractérise EXACTEMENT l'ensemble ℙ des nombres premiers — ni plus, ni moins — dans ses trois domaines d'application. » \\\\ — Synthèse formelle, fichier méthode\\_spectral.thy, juillet 2026` *(l.898)*
  - ❓ `json_chemin` → `Le théorème de synthèse est le point culminant du fichier methode\\_spectral.thy (version 3.42). Il constitue un ensemble à lui seul : il agrège les cinq faits indépendamment démontrés dans ce fichier en un seul énoncé unifié.` *(l.1017)*
  - ❓ `json_chemin` → `Le théorème de synthèse est le point culminant du fichier méthode\\_spectral.thy (version 3.42). Il constitue un ensemble à lui seul : il agrège les cinq faits indépendamment démontrés dans ce fichier en un seul énoncé unifié.` *(l.1018)*
  - ❓ `json_chemin` → `Chacun de ces faits est déjà un théorème ou un lemme HOL prouvé dans les sections précédentes du fichier methode\\_spectral.thy. Le théorème de synthèse se contente de les assembler — il n'introduit aucun axiome nouveau.` *(l.1027)*
  - ❓ `json_chemin` → `Chacun de ces faits est déjà un théorème ou un femme HOL prouvé dans les sections précédentes du fichier méthode\\_spectral.thy. Le théorème de synthèse se contente de les assembler — il n'introduit aucun axiome nouveau.` *(l.1028)*
  - ❓ `json_chemin` → `(* Pour F1 et F3 : voir les lemmes du Pont Savard (Section XIII) dans methode_spectral.thy *)` *(l.1047)*
  - ❓ `json_chemin` → `(* Pour F1 et F3 : voir les femmes du Pont Bavard (Section XIII) dans méthode_spectral.thy *)` *(l.1048)*
  - ❓ `json_chemin` → `Fait & Énoncé & Source dans methode\\_spectral.thy` *(l.1057)*
  - ❓ `json_chemin` → `Fait & Énoncé & Source dans méthode\\_spectral.thy` *(l.1058)*
  - ❓ `json_chemin` → `Le tableau suivant constitue un index de navigation vers les six postulats fondamentaux et leurs réalisations formelles dans methode\\_spectral.thy :` *(l.1347)*
  - ❓ `json_chemin` → `Le tableau suivant constitue un index de navigation vers les six postulats fondamentaux et leurs réalisations formelles dans méthode\\_spectral.thy :` *(l.1348)*
  - ❓ `json_chemin` → `Copyright 2026 Philippe Thomas Savard \\\\ Le fichier methode\\_spectral.thy et le présent document sont distribués sous les termes de la Licence Apache, Version 2.0 (la « Licence »). Vous ne pouvez utiliser ce fichier qu'en conformité avec la Licence. \\\\ Vous pouvez obtenir une copie de la Licence à l'adresse : \\\\ http://www.apache.org/licenses/LICENSE-2.0 \\\\ Sauf si requis par la loi applicable ou convenu par écrit, le logiciel distribué sous la Licence est distribué « EN L'ÉTAT », SANS GARANTIES NI CONDITIONS D'AUCUNE SORTE, expresses ou implicites. Voir la Licence pour les dispositions spécifiques régissant les autorisations et limitations en vertu de la Licence. \\\\ Dépôt public : https://github.com/PhilippeThomasSavard/Agent-multiloop-Gabriel` *(l.1427)*
  - ❓ `json_chemin` → `Copyright 2026 Philippe Thorax Bavard \\\\ Le fichier méthode\\_spectral.thy et le présent document sont distribués sous les termes de la Licence Apache, Version 2.0 (la « Licence »). Vous ne pouvez utiliser ce fichier qu'en conformité avec la Licence. \\\\ Vous pouvez obtenir une copie de la Licence à l'adresse : \\\\ hâte://www.apache.org/licences/LICENSE-2.0 \\\\ Sauf si requis par la loi applicable ou convenu par écrit, le logiciel distribué sous la Licence est distribué « EN L'ÉTAT », SANS GARANTIES NI CONDITIONS D'AUCUNE SORTE, expresses ou implicites. Voir la Licence pour les dispositions spécifiques régissant les autorisations et limitations en vertu de la Licence. \\\\ Dépôt public : hôtes://github.com/PhilippeThomasSavard/Agent-multiloop-Gariez` *(l.1428)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026.toc`
- **Type :** autre
- **Taille :** 6.0 Ko
- **Modifié :** 2026-08-07 19:52:03
- **Lignes :** 56
- **Hash MD5 :** `27df3ab251cd`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026_styled.log`
- **Type :** autre
- **Taille :** 38.6 Ko
- **Modifié :** 2026-08-05 20:06:00
- **Lignes :** 1069
- **Hash MD5 :** `110ad3795067`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026_styled.pdf`
- **Type :** autre
- **Taille :** 360.8 Ko
- **Modifié :** 2026-08-05 20:06:00
- **Hash MD5 :** `5d424558d9e2`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026_styled_v2.log`
- **Type :** autre
- **Taille :** 56.0 Ko
- **Modifié :** 2026-08-05 20:07:59
- **Lignes :** 1562
- **Hash MD5 :** `de1d0119449d`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026_styled_v2.pdf`
- **Type :** autre
- **Taille :** 375.3 Ko
- **Modifié :** 2026-08-05 20:07:59
- **Hash MD5 :** `285c3013a9e1`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026_styled_v3.log`
- **Type :** autre
- **Taille :** 57.0 Ko
- **Modifié :** 2026-08-05 20:25:26
- **Lignes :** 1592
- **Hash MD5 :** `cf89d45f8184`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_Brouillon_2026_styled_v3.pdf`
- **Type :** autre
- **Taille :** 391.3 Ko
- **Modifié :** 2026-08-05 20:25:26
- **Hash MD5 :** `98c5104d9c5c`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\Geometrie_du_Spectre_des_Nombres_Premiers_aout_08_2026.pdf`
- **Type :** autre
- **Taille :** 463.3 Ko
- **Modifié :** 2026-08-07 19:52:04
- **Hash MD5 :** `c4cd966d6023`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\geometrie_du_spectre_des_nombres_premiers.pdf`
- **Type :** autre
- **Taille :** 391.3 Ko
- **Modifié :** 2026-08-05 21:06:07
- **Hash MD5 :** `98c5104d9c5c`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\archives\texput.log`
- **Type :** autre
- **Taille :** 911.0 o
- **Modifié :** 2026-08-07 09:15:15
- **Lignes :** 23
- **Hash MD5 :** `23f7d09d5c93`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\convert_docx_to_latex.py`
- **Type :** python
- **Taille :** 10.2 Ko
- **Modifié :** 2026-08-05 21:06:07
- **Lignes :** 317
- **Hash MD5 :** `4601e0bab6e9`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.10)*
  - ❓ `import_module` → `argparse` *(l.12)*
  - ❓ `import_module` → `re` *(l.14)*
  - ❓ `import_module` → `zipfile` *(l.15)*
  - ❓ `import_module` → `xml.etree.ElementTree` *(l.16)*
  - ❓ `import_module` → `pathlib` *(l.17)*
  - ❓ `chemin_litteral` → `.//w:t` *(l.150)*

### `agent-multiloop-Gabriel-local\theories\tex\tex_quality\README.md`
- **Type :** markdown
- **Taille :** 2.4 Ko
- **Modifié :** 2026-08-06 07:55:03
- **Lignes :** 74
- **Hash MD5 :** `9b1a5a92acc2`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\tex\tex_quality\quality_pipeline.py`
- **Type :** python
- **Taille :** 21.1 Ko
- **Modifié :** 2026-08-15 14:56:42
- **Lignes :** 625
- **Hash MD5 :** `5f343b50341c`
- **Références sortantes (18) :**
  - ❓ `import_module` → `__future__` *(l.11)*
  - ❓ `import_module` → `argparse` *(l.13)*
  - ❓ `import_module` → `csv` *(l.15)*
  - ❓ `import_module` → `json` *(l.16)*
  - ❓ `import_module` → `math` *(l.17)*
  - ❓ `import_module` → `re` *(l.18)*
  - ❓ `import_module` → `shutil` *(l.19)*
  - ❓ `import_module` → `subprocess` *(l.20)*
  - ❓ `import_module` → `sys` *(l.21)*
  - ❓ `import_module` → `collections` *(l.22)*
  - ❓ `import_module` → `dataclasses` *(l.23)*
  - ❓ `import_module` → `pathlib` *(l.24)*
  - ❓ `import_module` → `typing` *(l.25)*
  - ❓ `import_module` → `spellchecker` *(l.42)*
  - ❓ `import_module` → `language_tool_python` *(l.246)*
  - ❓ `open_fichier` → `r` *(l.109)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\tex\tex_quality\README.md` *(l.69)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\scripts\tex_healthcheck.py` *(l.585)*

### `agent-multiloop-Gabriel-local\theories\tex\tex_quality\style_profile.py`
- **Type :** python
- **Taille :** 3.0 Ko
- **Modifié :** 2026-08-15 14:55:39
- **Lignes :** 94
- **Hash MD5 :** `691165e746b1`
- **Références sortantes (7) :**
  - ❓ `import_module` → `__future__` *(l.7)*
  - ❓ `import_module` → `argparse` *(l.9)*
  - ❓ `import_module` → `json` *(l.11)*
  - ❓ `import_module` → `re` *(l.12)*
  - ❓ `import_module` → `collections` *(l.13)*
  - ❓ `import_module` → `pathlib` *(l.14)*
  - ❓ `import_module` → `statistics` *(l.15)*

### `agent-multiloop-Gabriel-local\theories\tex\tex_quality\termbase_ca_qc.csv`
- **Type :** autre
- **Taille :** 618.0 o
- **Modifié :** 2026-08-06 07:37:55
- **Lignes :** 7
- **Hash MD5 :** `da36b95e5d6d`
- **Références sortantes :** *(aucune)*

### `agent-multiloop-Gabriel-local\theories\validation_hol_unifiee.thy`
- **Type :** isabelle
- **Taille :** 13.9 Ko
- **Modifié :** 2026-08-15 00:13:39
- **Lignes :** 384
- **Hash MD5 :** `5d100c13db9f`
- **Références sortantes (5) :**
  - ✅ `thy_import` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.16)*
  - ❓ `thy_import` → `Complex_Main` *(l.16)*
  - ❓ `thy_import` → `Real` *(l.16)*
  - ❓ `thy_ref_croisee` → `Complex` *(l.106)*
  - ❓ `thy_ref_croisee` → `Real` *(l.111)*

### `agent-multiloop-Gabriel-local\theories\verify_thy_structure.py`
- **Type :** python
- **Taille :** 31.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 847
- **Hash MD5 :** `eb8037f048eb`
- **Références sortantes (15) :**
  - ❓ `import_module` → `__future__` *(l.34)*
  - ❓ `import_module` → `argparse` *(l.35)*
  - ❓ `import_module` → `json` *(l.37)*
  - ❓ `import_module` → `re` *(l.38)*
  - ❓ `import_module` → `sys` *(l.39)*
  - ❓ `import_module` → `dataclasses` *(l.40)*
  - ❓ `import_module` → `pathlib` *(l.41)*
  - ❓ `import_module` → `typing` *(l.42)*
  - ❓ `import_module` → `rich.console` *(l.45)*
  - ❓ `import_module` → `rich.panel` *(l.46)*
  - ❓ `import_module` → `rich.table` *(l.47)*
  - ❓ `import_module` → `rich.text` *(l.48)*
  - ❓ `chemin_litteral` → `Un probleme detecte dans le fichier .thy` *(l.220)*
  - ❓ `chemin_litteral` → `Rapport agrege pour un fichier .thy` *(l.232)*
  - ❓ `chemin_litteral` → `*.thy` *(l.764)*

### `apply_patch.ps1`
- **Type :** autre
- **Taille :** 1.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 49
- **Hash MD5 :** `116f6fe8e899`
- **Références sortantes :** *(aucune)*

### `backend\requirements.txt`
- **Type :** texte
- **Taille :** 475.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 28
- **Hash MD5 :** `dc4f41965c33`
- **Références sortantes :** *(aucune)*

### `backend\server.py`
- **Type :** python
- **Taille :** 2.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 89
- **Hash MD5 :** `871f87afa15e`
- **Références sortantes (12) :**
  - ❓ `import_module` → `fastapi` *(l.1)*
  - ❓ `import_module` → `dotenv` *(l.2)*
  - ❓ `import_module` → `starlette.middleware.cors` *(l.3)*
  - ❓ `import_module` → `motor.motor_asyncio` *(l.4)*
  - ❓ `import_module` → `os` *(l.5)*
  - ❓ `import_module` → `logging` *(l.6)*
  - ❓ `import_module` → `pathlib` *(l.7)*
  - ❓ `import_module` → `pydantic` *(l.8)*
  - ❓ `import_module` → `typing` *(l.9)*
  - ❓ `import_module` → `uuid` *(l.10)*
  - ❓ `import_module` → `datetime` *(l.11)*
  - ❓ `chemin_litteral` → `/status` *(l.45)*

### `declaration_securite.md`
- **Type :** markdown
- **Taille :** 8.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 197
- **Hash MD5 :** `a3261528c1f1`
- **Références sortantes (2) :**
  - ✅ `ref_generique` → `SECURITY.md` *(l.3)*
  - ❓ `ref_generique` → `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local/issues/new` *(l.89)*

### `deploy_gabriel_v6.py`
- **Type :** python
- **Taille :** 3.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 137
- **Hash MD5 :** `fbbb95c3920d`
- **Références sortantes (6) :**
  - ❓ `import_module` → `sys` *(l.7)*
  - ❓ `import_module` → `pathlib` *(l.9)*
  - ❓ `import_module` → `dotenv` *(l.23)*
  - ❓ `import_module` → `os` *(l.25)*
  - ❓ `import_module` → `src.gabriel_llm_integration_v2` *(l.49)*
  - ❓ `chemin_litteral` → `\n[STEP 1] Vérifier .env` *(l.21)*

### `docs\.nojekyll`
- **Type :** autre
- **Taille :** 141.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 3
- **Hash MD5 :** `98e0c36f9d35`
- **Références sortantes :** *(aucune)*

### `docs\README.md`
- **Type :** markdown
- **Taille :** 1007.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 29
- **Hash MD5 :** `c927b2b72c87`
- **Références sortantes (1) :**
  - ❓ `ref_generique` → `//2racinede4carreunivers-dev.github.io/agent-multiloop-Gabriel-local/` *(l.14)*

### `docs\index.html`
- **Type :** html
- **Taille :** 14.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 337
- **Hash MD5 :** `3a6fdf4fc8c7`
- **Références sortantes (7) :**
  - ❓ `ref_generique` → `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local` *(l.202)*
  - ❓ `ref_generique` → `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local/releases` *(l.203)*
  - ❓ `ref_generique` → `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local/blob/main/agent-multiloop-Gabriel-local/theories/methode_spectral.thy` *(l.204)*
  - ❓ `ref_generique` → `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local.git` *(l.280)*
  - ❓ `ref_generique` → `//www.apache.org/licenses/LICENSE-2.0` *(l.291)*
  - ❓ `ref_generique` → `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local/actions` *(l.329)*
  - ❓ `ref_generique` → `//github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local/blob/main/LICENSE` *(l.331)*

### `fichier_terminal_test_gabriel.docx`
- **Type :** autre
- **Taille :** 30.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Hash MD5 :** `ec1a2a1ff47b`
- **Références sortantes :** *(aucune)*

### `find_debugger.py`
- **Type :** python
- **Taille :** 537.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `55118dd25748`
- **Références sortantes (2) :**
  - ❓ `import_module` → `os` *(l.2)*
  - ✅ `open_fichier` → `agent-multiloop-Gabriel-local\src\core\pipeline.py` *(l.5)*

### `fix_corrections.py`
- **Type :** python
- **Taille :** 2.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 66
- **Hash MD5 :** `1b44acf38643`
- **Références sortantes (2) :**
  - ❓ `import_module` → `re` *(l.6)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.10)*

### `fix_debugger.py`
- **Type :** python
- **Taille :** 2.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 46
- **Hash MD5 :** `adf55f5c9264`
- **Références sortantes (2) :**
  - ❓ `import_module` → `os` *(l.3)*
  - ✅ `open_fichier` → `agent-multiloop-Gabriel-local\src\core\pipeline.py` *(l.8)*

### `fix_line_2605.py`
- **Type :** python
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 46
- **Hash MD5 :** `37309bcd62f8`
- **Références sortantes (1) :**
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.7)*

### `fix_theoretical_patterns.py`
- **Type :** python
- **Taille :** 3.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 70
- **Hash MD5 :** `b808667961c0`
- **Références sortantes (2) :**
  - ❓ `import_module` → `re` *(l.3)*
  - ✅ `chemin_litteral` → `agent-multiloop-Gabriel-local\src\multiloop\request_decomposer.py` *(l.7)*

### `frontend\.gitignore`
- **Type :** autre
- **Taille :** 333.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 24
- **Hash MD5 :** `62bf484f353e`
- **Références sortantes :** *(aucune)*

### `frontend\README.md`
- **Type :** markdown
- **Taille :** 3.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 71
- **Hash MD5 :** `47731d5d79e6`
- **Références sortantes (11) :**
  - ❓ `ref_generique` → `//github.com/facebook/create-react-app` *(l.3)*
  - ❓ `ref_generique` → `//localhost` *(l.12)*
  - ❓ `ref_generique` → `//facebook.github.io/create-react-app/docs/running-tests` *(l.20)*
  - ❓ `ref_generique` → `//facebook.github.io/create-react-app/docs/deployment` *(l.30)*
  - ❓ `ref_generique` → `//facebook.github.io/create-react-app/docs/getting-started` *(l.44)*
  - ❓ `ref_generique` → `//reactjs.org/` *(l.46)*
  - ❓ `ref_generique` → `//facebook.github.io/create-react-app/docs/code-splitting` *(l.50)*
  - ❓ `ref_generique` → `//facebook.github.io/create-react-app/docs/analyzing-the-bundle-size` *(l.54)*
  - ❓ `ref_generique` → `//facebook.github.io/create-react-app/docs/making-a-progressive-web-app` *(l.58)*
  - ❓ `ref_generique` → `//facebook.github.io/create-react-app/docs/advanced-configuration` *(l.62)*
  - ❓ `ref_generique` → `//facebook.github.io/create-react-app/docs/troubleshooting` *(l.70)*

### `frontend\components.json`
- **Type :** json
- **Taille :** 464.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 21
- **Hash MD5 :** `2b244abb0827`
- **Références sortantes (1) :**
  - ❓ `json_chemin` → `https://ui.shadcn.com/schema.json` *(l.2)*

### `frontend\craco.config.js`
- **Type :** javascript
- **Taille :** 2.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 101
- **Hash MD5 :** `be0ff4ecf25e`
- **Références sortantes (3) :**
  - ❓ `ref_generique` → `process.env` *(l.7)*
  - ❓ `ref_generique` → `./plugins/health-check/webpack-health-plugin` *(l.20)*
  - ❓ `ref_generique` → `./plugins/health-check/health-endpoints` *(l.21)*

### `frontend\jsconfig.json`
- **Type :** json
- **Taille :** 124.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 9
- **Hash MD5 :** `ab2698309edf`
- **Références sortantes :** *(aucune)*

### `frontend\package.json`
- **Type :** json
- **Taille :** 3.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 99
- **Hash MD5 :** `ee74fefad626`
- **Références sortantes (1) :**
  - ❓ `json_chemin` → `https://assets.emergent.sh/npm/emergentbase-visual-edits-1.0.8.tgz` *(l.83)*

### `frontend\plugins\health-check\health-endpoints.js`
- **Type :** javascript
- **Taille :** 7.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 214
- **Hash MD5 :** `704dd5d09710`
- **Références sortantes (8) :**
  - ❓ `ref_generique` → `/health` *(l.27)*
  - ❓ `ref_generique` → `res.json` *(l.34)*
  - ❓ `ref_generique` → `process.env` *(l.78)*
  - ❓ `ref_generique` → `/health/simple` *(l.83)*
  - ❓ `ref_generique` → `/health/ready` *(l.100)*
  - ❓ `ref_generique` → `/health/live` *(l.122)*
  - ❓ `ref_generique` → `/health/errors` *(l.132)*
  - ❓ `ref_generique` → `/health/stats` *(l.147)*

### `frontend\plugins\health-check\webpack-health-plugin.js`
- **Type :** javascript
- **Taille :** 3.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 121
- **Hash MD5 :** `0f312267003a`
- **Références sortantes :** *(aucune)*

### `frontend\postcss.config.js`
- **Type :** javascript
- **Taille :** 88.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 7
- **Hash MD5 :** `762a94d1749c`
- **Références sortantes :** *(aucune)*

### `frontend\public\index.html`
- **Type :** html
- **Taille :** 6.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 114
- **Hash MD5 :** `3cfce5fec57f`
- **Références sortantes (10) :**
  - ❓ `ref_generique` → `emergent.sh` *(l.7)*
  - ❓ `ref_generique` → `//fonts.googleapis.com` *(l.8)*
  - ❓ `ref_generique` → `//fonts.gstatic.com` *(l.9)*
  - ❓ `ref_generique` → `//fonts.googleapis.com/css2` *(l.10)*
  - ❓ `ref_generique` → `manifest.json` *(l.12)*
  - ❓ `ref_generique` → `//developers.google.com/web/fundamentals/web-app-manifest/` *(l.13)*
  - ❓ `ref_generique` → `/favicon.ico` *(l.20)*
  - ❓ `ref_generique` → `//assets.emergent.sh/scripts/emergent-main.js` *(l.26)*
  - ❓ `ref_generique` → `/static/array.js` *(l.70)*
  - ❓ `ref_generique` → `//us.i.posthog.com` *(l.104)*

### `frontend\src\App.css`
- **Type :** css
- **Taille :** 612.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 35
- **Hash MD5 :** `3c41638b5f04`
- **Références sortantes :** *(aucune)*

### `frontend\src\App.js`
- **Type :** javascript
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 57
- **Hash MD5 :** `ac8fb87c08e0`
- **Références sortantes (3) :**
  - ❓ `ref_generique` → `process.env` *(l.7)*
  - ❓ `ref_generique` → `//emergent.sh` *(l.30)*
  - ❓ `ref_generique` → `//avatars.githubusercontent.com/in/1201222` *(l.34)*

### `frontend\src\agent-local-ia-carre\.gitconfig`
- **Type :** autre
- **Taille :** 64.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 4
- **Hash MD5 :** `afb33b54b84a`
- **Références sortantes :** *(aucune)*

### `frontend\src\agent-local-ia-carre\arbo.txt`
- **Type :** texte
- **Taille :** 264.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 6455
- **Hash MD5 :** `3a71e8ec3306`
- **Références sortantes :** *(aucune)*

### `frontend\src\agent-local-ia-carre\yarn.lock`
- **Type :** autre
- **Taille :** 90.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 5
- **Hash MD5 :** `d4ebe8f48dbf`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\accordion.jsx`
- **Type :** autre
- **Taille :** 1.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `415118b06768`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\alert-dialog.jsx`
- **Type :** autre
- **Taille :** 3.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 98
- **Hash MD5 :** `9a4bd38fdada`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\alert.jsx`
- **Type :** autre
- **Taille :** 1.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 48
- **Hash MD5 :** `207fa30ee81f`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\aspect-ratio.jsx`
- **Type :** autre
- **Taille :** 145.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 6
- **Hash MD5 :** `114d53f29a18`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\avatar.jsx`
- **Type :** autre
- **Taille :** 1.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 34
- **Hash MD5 :** `b8020660ae3b`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\badge.jsx`
- **Type :** autre
- **Taille :** 1.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 35
- **Hash MD5 :** `6d218c99805c`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\breadcrumb.jsx`
- **Type :** autre
- **Taille :** 2.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 93
- **Hash MD5 :** `5b4a8a8dff8c`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\button.jsx`
- **Type :** autre
- **Taille :** 1.7 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 49
- **Hash MD5 :** `5702a92b8fc7`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\calendar.jsx`
- **Type :** autre
- **Taille :** 2.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 72
- **Hash MD5 :** `31053e4f709a`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\card.jsx`
- **Type :** autre
- **Taille :** 1.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 51
- **Hash MD5 :** `cebc57b73ad5`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\carousel.jsx`
- **Type :** autre
- **Taille :** 4.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 194
- **Hash MD5 :** `6fa103c35cad`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\checkbox.jsx`
- **Type :** autre
- **Taille :** 902.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 23
- **Hash MD5 :** `36f395a09cf7`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\collapsible.jsx`
- **Type :** autre
- **Taille :** 324.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 10
- **Hash MD5 :** `1048c23a2aad`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\command.jsx`
- **Type :** autre
- **Taille :** 3.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 117
- **Hash MD5 :** `1e0805fc80b7`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\context-menu.jsx`
- **Type :** autre
- **Taille :** 6.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 157
- **Hash MD5 :** `927b19737172`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\dialog.jsx`
- **Type :** autre
- **Taille :** 3.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 95
- **Hash MD5 :** `c29e6b997d54`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\drawer.jsx`
- **Type :** autre
- **Taille :** 2.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 91
- **Hash MD5 :** `b701be48abdc`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\dropdown-menu.jsx`
- **Type :** autre
- **Taille :** 6.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 157
- **Hash MD5 :** `c0dd3c80defc`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\form.jsx`
- **Type :** autre
- **Taille :** 3.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 134
- **Hash MD5 :** `e547b559587f`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\hover-card.jsx`
- **Type :** autre
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 24
- **Hash MD5 :** `76add5fbadc9`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\input-otp.jsx`
- **Type :** autre
- **Taille :** 1.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 54
- **Hash MD5 :** `3d1077cc27ba`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\input.jsx`
- **Type :** autre
- **Taille :** 707.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 20
- **Hash MD5 :** `68a1da1b9b9a`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\label.jsx`
- **Type :** autre
- **Taille :** 541.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 17
- **Hash MD5 :** `cb2728638eb5`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\menubar.jsx`
- **Type :** autre
- **Taille :** 6.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 199
- **Hash MD5 :** `4fdb8d382f16`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\navigation-menu.jsx`
- **Type :** autre
- **Taille :** 4.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 105
- **Hash MD5 :** `73a7af62957b`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\pagination.jsx`
- **Type :** autre
- **Taille :** 2.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 101
- **Hash MD5 :** `75fb604ebfe9`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\popover.jsx`
- **Type :** autre
- **Taille :** 1.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 28
- **Hash MD5 :** `fe57a241245d`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\progress.jsx`
- **Type :** autre
- **Taille :** 674.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `f1e8b9ebd676`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\radio-group.jsx`
- **Type :** autre
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 30
- **Hash MD5 :** `9247a41d5b67`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\resizable.jsx`
- **Type :** autre
- **Taille :** 1.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 41
- **Hash MD5 :** `624b0e0046ff`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\scroll-area.jsx`
- **Type :** autre
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 39
- **Hash MD5 :** `3a1fc9eb76c5`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\select.jsx`
- **Type :** autre
- **Taille :** 4.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 120
- **Hash MD5 :** `59bc251efe75`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\separator.jsx`
- **Type :** autre
- **Taille :** 623.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 24
- **Hash MD5 :** `53ad02ebb72b`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\sheet.jsx`
- **Type :** autre
- **Taille :** 3.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 109
- **Hash MD5 :** `6b2f7344da81`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\skeleton.jsx`
- **Type :** autre
- **Taille :** 239.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 15
- **Hash MD5 :** `21ae0c4be942`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\slider.jsx`
- **Type :** autre
- **Taille :** 935.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 22
- **Hash MD5 :** `080b174fd379`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\sonner.jsx`
- **Type :** autre
- **Taille :** 825.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 29
- **Hash MD5 :** `fddad34374a9`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\switch.jsx`
- **Type :** autre
- **Taille :** 1.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 23
- **Hash MD5 :** `d3280805fe8f`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\table.jsx`
- **Type :** autre
- **Taille :** 2.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 87
- **Hash MD5 :** `c62cc8e3aee4`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\tabs.jsx`
- **Type :** autre
- **Taille :** 1.5 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `1b3bfe26cd49`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\textarea.jsx`
- **Type :** autre
- **Taille :** 603.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 19
- **Hash MD5 :** `17dee4732837`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\toast.jsx`
- **Type :** autre
- **Taille :** 3.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 86
- **Hash MD5 :** `86c01a786d29`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\toaster.jsx`
- **Type :** autre
- **Taille :** 807.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 34
- **Hash MD5 :** `61315896aeeb`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\toggle-group.jsx`
- **Type :** autre
- **Taille :** 1.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 44
- **Hash MD5 :** `b664f5e0e42e`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\toggle.jsx`
- **Type :** autre
- **Taille :** 1.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 41
- **Hash MD5 :** `00fd341e7d7f`
- **Références sortantes :** *(aucune)*

### `frontend\src\components\ui\tooltip.jsx`
- **Type :** autre
- **Taille :** 1.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 27
- **Hash MD5 :** `0e4e8301d3f1`
- **Références sortantes :** *(aucune)*

### `frontend\src\constants\testIds\auth.js`
- **Type :** javascript
- **Taille :** 1.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 34
- **Hash MD5 :** `958eb4f290a0`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `frontend\src\constants\testIds\index.js` *(l.2)*

### `frontend\src\constants\testIds\home.js`
- **Type :** javascript
- **Taille :** 217.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 7
- **Hash MD5 :** `35f389dca6d0`
- **Références sortantes (1) :**
  - ✅ `ref_generique` → `frontend\src\constants\testIds\auth.js` *(l.2)*

### `frontend\src\constants\testIds\index.js`
- **Type :** javascript
- **Taille :** 715.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 16
- **Hash MD5 :** `4dbd4e489b6e`
- **Références sortantes (3) :**
  - ❓ `ref_generique` → `./<feature>` *(l.12)*
  - ❓ `ref_generique` → `./auth` *(l.14)*
  - ❓ `ref_generique` → `./home` *(l.15)*

### `frontend\src\hooks\use-toast.js`
- **Type :** javascript
- **Taille :** 3.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 156
- **Hash MD5 :** `df175c0decac`
- **Références sortantes :** *(aucune)*

### `frontend\src\index.css`
- **Type :** css
- **Taille :** 3.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 116
- **Hash MD5 :** `cd140071f13c`
- **Références sortantes :** *(aucune)*

### `frontend\src\index.js`
- **Type :** javascript
- **Taille :** 578.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 24
- **Hash MD5 :** `428dd3a9fe95`
- **Références sortantes :** *(aucune)*

### `frontend\src\lib\utils.js`
- **Type :** javascript
- **Taille :** 143.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 7
- **Hash MD5 :** `eff53006b93c`
- **Références sortantes :** *(aucune)*

### `frontend\tailwind.config.js`
- **Type :** javascript
- **Taille :** 2.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 82
- **Hash MD5 :** `1915f2cc371f`
- **Références sortantes (2) :**
  - ❓ `ref_generique` → `./src/**/*.{js,jsx,ts,tsx}` *(l.5)*
  - ✅ `ref_generique` → `frontend\public\index.html` *(l.6)*

### `frontend\yarn.lock`
- **Type :** autre
- **Taille :** 530.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 11362
- **Hash MD5 :** `0f66b9b9a693`
- **Références sortantes :** *(aucune)*

### `gabriel_repo_mapper.py`
- **Type :** python
- **Taille :** 29.3 Ko
- **Modifié :** 2026-08-17 10:50:53
- **Lignes :** 718
- **Hash MD5 :** `4923c1379926`
- **Références sortantes (15) :**
  - ❓ `import_module` → `os` *(l.11)*
  - ❓ `import_module` → `re` *(l.13)*
  - ❓ `import_module` → `sys` *(l.14)*
  - ❓ `import_module` → `json` *(l.15)*
  - ❓ `import_module` → `argparse` *(l.16)*
  - ❓ `import_module` → `hashlib` *(l.17)*
  - ❓ `import_module` → `pathlib` *(l.18)*
  - ❓ `import_module` → `datetime` *(l.19)*
  - ❓ `import_module` → `collections` *(l.20)*
  - ❓ `open_fichier` → `chemin` *(l.93)*
  - ❓ `open_fichier` → `gabriel_repo_map.json` *(l.708)*
  - ✅ `Path()` → `.` *(l.100)*
  - ❓ `chemin_litteral` → `gabriel_repo_report.md` *(l.681)*
  - ✅ `base_donnees` → `.` *(l.123)*
  - ❓ `base_donnees` → `sqlite:///...` *(l.123)*

### `memory\.gitkeep`
- **Type :** autre
- **Taille :** 0.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 1
- **Hash MD5 :** `d41d8cd98f00`
- **Références sortantes :** *(aucune)*

### `memory\PRD.md`
- **Type :** markdown
- **Taille :** 83.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 856
- **Hash MD5 :** `7ab0c54a1cb7`
- **Références sortantes (34) :**
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\theories\methode_spectral.thy` *(l.7)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\engines\question_graphs.py` *(l.62)*
  - ❓ `ref_generique` → `iteration_15.json` *(l.187)*
  - ❓ `ref_generique` → `iteration_14.json` *(l.200)*
  - ❓ `ref_generique` → `iteration_13.json` *(l.226)*
  - ❓ `ref_generique` → `iteration_12.json` *(l.246)*
  - ❓ `ref_generique` → `iteration_11.json` *(l.265)*
  - ❓ `ref_generique` → `iteration_10.json` *(l.303)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\CONFIG_ENV_GUIDE.md` *(l.334)*
  - ❓ `ref_generique` → `/theories` *(l.335)*
  - ❓ `ref_generique` → `/home/agent/app/theories` *(l.335)*
  - ❓ `ref_generique` → `/app/...` *(l.335)*
  - ❓ `ref_generique` → `/home/agent/app/CONFIG_ENV_GUIDE.md` *(l.338)*
  - ❓ `ref_generique` → `/home/agent/app/scripts` *(l.340)*
  - ❓ `ref_generique` → `/home/agent/app/memory` *(l.352)*
  - ❓ `ref_generique` → `/home/agent/app/data/debats-onedrive` *(l.373)*
  - ❓ `ref_generique` → `/app/agent-multiloop-Gabriel-local/` *(l.383)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\docker-compose.yml` *(l.386)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\main_cli.py` *(l.388)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\ui\cli.py` *(l.403)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\ui\ci_status.py` *(l.404)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\ui\debug_session.py` *(l.405)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\visualization\curves.py` *(l.407)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\visualization\ascii_renderer.py` *(l.408)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\visualization\rich_renderer.py` *(l.409)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\visualization\png_renderer.py` *(l.410)*
  - ❓ `ref_generique` → `emergent.sh` *(l.426)*
  - ❓ `ref_generique` → `/home/agent/app/.env` *(l.489)*
  - ❓ `ref_generique` → `./.env:/home/agent/app/.env:ro`` *(l.498)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\HOL_ISABELLE_FIX.md` *(l.808)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\adapters\hol_integration.py` *(l.808)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\src\spectral\hol_script_generator.py` *(l.808)*
  - ✅ `ref_generique` → `agent-multiloop-Gabriel-local\examples\verif_p103_n27_CORRECT.thy` *(l.808)*
  - ✅ `ref_generique` → `README.md` *(l.840)*

### `memory\__init__.py`
- **Type :** python
- **Taille :** 1.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 59
- **Hash MD5 :** `5e654d0a9d3c`
- **Références sortantes (3) :**
  - ❓ `import_module` → `.memoire_conceptuelle` *(l.4)*
  - ❓ `import_module` → `.memoire_technique` *(l.14)*
  - ❓ `import_module` → `.gestionnaire_erreurs` *(l.24)*

### `memory\adaptateur_cognitif_rag.py`
- **Type :** python
- **Taille :** 13.8 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 336
- **Hash MD5 :** `85a4d10e2ed4`
- **Références sortantes (7) :**
  - ❓ `import_module` → `json` *(l.5)*
  - ❓ `import_module` → `re` *(l.7)*
  - ❓ `import_module` → `logging` *(l.8)*
  - ❓ `import_module` → `typing` *(l.9)*
  - ❓ `import_module` → `pathlib` *(l.10)*
  - ❓ `import_module` → `memory.dictionnaire_spectral` *(l.86)*
  - ❓ `chemin_litteral` → `memory/dictionnaire_spectral.json` *(l.20)*

### `memory\comparaison_asymetrique_ordonnee.py`
- **Type :** python
- **Taille :** 7.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 220
- **Hash MD5 :** `fea6a8a0b945`
- **Références sortantes (2) :**
  - ❓ `import_module` → `typing` *(l.16)*
  - ❓ `import_module` → `numpy` *(l.18)*

### `memory\dictionnaire_spectral.py`
- **Type :** python
- **Taille :** 15.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 349
- **Hash MD5 :** `62a3c4ca7033`
- **Références sortantes (3) :**
  - ❓ `import_module` → `json` *(l.5)*
  - ❓ `import_module` → `pathlib` *(l.7)*
  - ❓ `chemin_litteral` → `memory/dictionnaire_spectral.json` *(l.318)*

### `memory\directives_theorie_savard.md`
- **Type :** markdown
- **Taille :** 9.0 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 299
- **Hash MD5 :** `faa0ee577c4d`
- **Références sortantes (1) :**
  - ❓ `ref_generique` → `//github.com/2racinede4carreunivers-dev/` *(l.162)*

### `memory\error_cache\errors.json`
- **Type :** json
- **Taille :** 1.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 42
- **Hash MD5 :** `39e5d655f1a6`
- **Références sortantes :** *(aucune)*

### `memory\gestionnaire_erreurs.py`
- **Type :** python
- **Taille :** 12.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 315
- **Hash MD5 :** `7d719e6b1f55`
- **Références sortantes (7) :**
  - ❓ `import_module` → `json` *(l.12)*
  - ❓ `import_module` → `typing` *(l.14)*
  - ❓ `import_module` → `dataclasses` *(l.15)*
  - ❓ `import_module` → `datetime` *(l.16)*
  - ❓ `import_module` → `pathlib` *(l.17)*
  - ❓ `import_module` → `enum` *(l.18)*
  - ✅ `chemin_litteral` → `memory\error_cache\errors.json` *(l.68)*

### `memory\memoire_conceptuelle.py`
- **Type :** python
- **Taille :** 11.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 307
- **Hash MD5 :** `617886ff4d49`
- **Références sortantes (3) :**
  - ❓ `import_module` → `typing` *(l.13)*
  - ❓ `import_module` → `dataclasses` *(l.15)*
  - ❓ `import_module` → `enum` *(l.16)*

### `memory\memoire_technique.py`
- **Type :** python
- **Taille :** 14.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 376
- **Hash MD5 :** `8e432d46b3e6`
- **Références sortantes (7) :**
  - ❓ `import_module` → `typing` *(l.13)*
  - ❓ `import_module` → `dataclasses` *(l.15)*
  - ❓ `import_module` → `enum` *(l.16)*
  - ❓ `chemin_litteral` → `prime_arithmetic.thy` *(l.198)*
  - ❓ `chemin_litteral` → `regime_definitions.thy` *(l.211)*
  - ❓ `chemin_litteral` → `gap_properties.thy` *(l.225)*
  - ❓ `chemin_litteral` → `harmonie_lemmas.thy` *(l.239)*

### `memory\prompt_injector.py`
- **Type :** python
- **Taille :** 9.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 295
- **Hash MD5 :** `c2c49739c5e6`
- **Références sortantes (6) :**
  - ❓ `import_module` → `logging` *(l.5)*
  - ❓ `import_module` → `typing` *(l.7)*
  - ❓ `import_module` → `dataclasses` *(l.8)*
  - ❓ `import_module` → `sys` *(l.9)*
  - ❓ `import_module` → `pathlib` *(l.10)*
  - ❓ `import_module` → `memory.theory_axioms_manager` *(l.14)*

### `memory\prompt_injector_enhanced.py`
- **Type :** python
- **Taille :** 15.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 440
- **Hash MD5 :** `e3993699ce18`
- **Références sortantes (6) :**
  - ❓ `import_module` → `logging` *(l.5)*
  - ❓ `import_module` → `typing` *(l.7)*
  - ❓ `import_module` → `dataclasses` *(l.8)*
  - ❓ `import_module` → `sys` *(l.9)*
  - ❓ `import_module` → `pathlib` *(l.10)*
  - ❓ `import_module` → `memory.theory_axioms_manager` *(l.14)*

### `memory\test_credentials.md`
- **Type :** markdown
- **Taille :** 201.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 4
- **Hash MD5 :** `29e12010be12`
- **Références sortantes :** *(aucune)*

### `memory\theory_axioms_manager.py`
- **Type :** python
- **Taille :** 13.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 403
- **Hash MD5 :** `b53eef18a58f`
- **Références sortantes (9) :**
  - ❓ `import_module` → `logging` *(l.5)*
  - ❓ `import_module` → `typing` *(l.7)*
  - ❓ `import_module` → `pathlib` *(l.8)*
  - ❓ `import_module` → `dataclasses` *(l.9)*
  - ❓ `import_module` → `json` *(l.10)*
  - ❓ `import_module` → `yaml` *(l.11)*
  - ❓ `chemin_litteral` → `Charge directives depuis memory/directives_theorie_savard.md` *(l.49)*
  - ✅ `chemin_litteral` → `memory\directives_theorie_savard.md` *(l.51)*
  - ❓ `chemin_litteral` → `memory/axioms.json` *(l.323)*

### `pdf\analyse_hypothese_riemann_savard.pdf`
- **Type :** autre
- **Taille :** 1.0 Mo
- **Modifié :** 2026-08-03 14:07:48
- **Hash MD5 :** `6f9f3ecd79d8`
- **Références sortantes :** *(aucune)*

### `quick-start.bat`
- **Type :** autre
- **Taille :** 993.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 33
- **Hash MD5 :** `7f110d4a0bc8`
- **Références sortantes :** *(aucune)*

### `security_validator.py`
- **Type :** python
- **Taille :** 9.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 276
- **Hash MD5 :** `3d40e056a82e`
- **Références sortantes (8) :**
  - ❓ `import_module` → `os` *(l.6)*
  - ❓ `import_module` → `sys` *(l.8)*
  - ❓ `import_module` → `re` *(l.9)*
  - ❓ `import_module` → `subprocess` *(l.10)*
  - ❓ `import_module` → `pathlib` *(l.11)*
  - ❓ `chemin_litteral` → `Valide .gitignore existe et contient .env` *(l.105)*
  - ❓ `chemin_litteral` → `✓ .gitignore contient .env` *(l.133)*
  - ❓ `chemin_litteral` → `  2. Consulter SECURITY_FIX.md` *(l.250)*

### `src\core\detecteur_asymetrique_ordonnee.py`
- **Type :** python
- **Taille :** 7.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 210
- **Hash MD5 :** `7a3b4a3d5b06`
- **Références sortantes (2) :**
  - ❓ `import_module` → `re` *(l.12)*
  - ❓ `chemin_litteral` → `utiliser comparaison_asymetrique_ordonnee.py` *(l.166)*

### `src\core\gabriel_comparaison_asymetrique.py`
- **Type :** python
- **Taille :** 5.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 149
- **Hash MD5 :** `a9ef8bb04f28`
- **Références sortantes (5) :**
  - ❓ `import_module` → `typing` *(l.10)*
  - ❓ `import_module` → `sys` *(l.12)*
  - ❓ `import_module` → `pathlib` *(l.13)*
  - ✅ `import_module` → `memory\comparaison_asymetrique_ordonnee.py` *(l.17)*
  - ❓ `import_module` → `re` *(l.51)*

### `src\core\gabriel_geometric_wrapper.py`
- **Type :** python
- **Taille :** 7.4 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 222
- **Hash MD5 :** `7b33da2d4d1c`
- **Références sortantes (5) :**
  - ❓ `import_module` → `re` *(l.10)*
  - ❓ `import_module` → `typing` *(l.12)*
  - ❓ `import_module` → `src.core.metaphore_geometrique` *(l.13)*
  - ❓ `import_module` → `FreeCAD` *(l.154)*
  - ❓ `import_module` → `Part` *(l.155)*

### `src\core\generateur_schemas_avances.py`
- **Type :** python
- **Taille :** 17.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 440
- **Hash MD5 :** `66a86684deaa`
- **Références sortantes (3) :**
  - ❓ `import_module` → `typing` *(l.18)*
  - ❓ `import_module` → `enum` *(l.20)*
  - ❓ `import_module` → `math` *(l.21)*

### `src\core\integrateur_memoire.py`
- **Type :** python
- **Taille :** 12.6 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 321
- **Hash MD5 :** `27b472cfe82c`
- **Références sortantes (9) :**
  - ❓ `import_module` → `sys` *(l.13)*
  - ❓ `import_module` → `pathlib` *(l.15)*
  - ❓ `import_module` → `typing` *(l.16)*
  - ✅ `import_module` → `memory\memoire_conceptuelle.py` *(l.20)*
  - ✅ `import_module` → `memory\memoire_technique.py` *(l.28)*
  - ✅ `import_module` → `memory\gestionnaire_erreurs.py` *(l.38)*
  - ✅ `import_module` → `src\core\detecteur_asymetrique_ordonnee.py` *(l.49)*
  - ✅ `import_module` → `src\core\gabriel_comparaison_asymetrique.py` *(l.50)*
  - ❓ `import_module` → `datetime` *(l.180)*

### `src\core\integrateur_memoire_patch.py`
- **Type :** python
- **Taille :** 2.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 59
- **Hash MD5 :** `4e58cd2b73f8`
- **Références sortantes :** *(aucune)*

### `src\core\llm_router_explicite.py`
- **Type :** python
- **Taille :** 10.2 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 289
- **Hash MD5 :** `bbf621650977`
- **Références sortantes (7) :**
  - ❓ `import_module` → `os` *(l.14)*
  - ❓ `import_module` → `asyncio` *(l.16)*
  - ❓ `import_module` → `logging` *(l.17)*
  - ❓ `import_module` → `typing` *(l.18)*
  - ❓ `import_module` → `enum` *(l.19)*
  - ❓ `import_module` → `anthropic` *(l.165)*
  - ❓ `import_module` → `openai` *(l.199)*

### `src\core\metaphore_geometrique.py`
- **Type :** python
- **Taille :** 18.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 472
- **Hash MD5 :** `ef53a288bf74`
- **Références sortantes (4) :**
  - ❓ `import_module` → `numpy` *(l.19)*
  - ❓ `import_module` → `typing` *(l.21)*
  - ❓ `import_module` → `dataclasses` *(l.22)*
  - ❓ `import_module` → `enum` *(l.23)*

### `src\core\vision_gabriel.py`
- **Type :** python
- **Taille :** 14.3 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 405
- **Hash MD5 :** `ecbc73f44ec4`
- **Références sortantes (8) :**
  - ❓ `import_module` → `base64` *(l.23)*
  - ❓ `import_module` → `os` *(l.25)*
  - ❓ `import_module` → `typing` *(l.26)*
  - ❓ `import_module` → `pathlib` *(l.27)*
  - ❓ `import_module` → `enum` *(l.28)*
  - ❓ `import_module` → `sys` *(l.29)*
  - ❓ `Path()` → `/home/agent/app/images` *(l.61)*
  - ❓ `chemin_litteral` → `/home/agent/app/images/` *(l.120)*

### `test_gabriel_v6.1_gap_mixed.py`
- **Type :** python
- **Taille :** 5.1 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 176
- **Hash MD5 :** `06fe8af637de`
- **Références sortantes (5) :**
  - ❓ `import_module` → `sys` *(l.6)*
  - ❓ `import_module` → `pathlib` *(l.8)*
  - ❓ `import_module` → `src.gabriel_gap_mixed_handler` *(l.24)*
  - ❓ `import_module` → `src.hol4_gap_mixed_generator` *(l.28)*
  - ❓ `import_module` → `traceback` *(l.173)*

### `test_imports.py`
- **Type :** python
- **Taille :** 870.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 29
- **Hash MD5 :** `77157509a4bd`
- **Références sortantes (3) :**
  - ❓ `import_module` → `sys` *(l.3)*
  - ❓ `import_module` → `pathlib` *(l.5)*
  - ✅ `import_module` → `src\core\detecteur_asymetrique_ordonnee.py` *(l.11)*

### `test_reports\.gitkeep`
- **Type :** autre
- **Taille :** 0.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 1
- **Hash MD5 :** `d41d8cd98f00`
- **Références sortantes :** *(aucune)*

### `test_reports\pytest\.gitkeep`
- **Type :** autre
- **Taille :** 0.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 1
- **Hash MD5 :** `d41d8cd98f00`
- **Références sortantes :** *(aucune)*

### `test_systeme_memoire_complet.py`
- **Type :** python
- **Taille :** 5.9 Ko
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 185
- **Hash MD5 :** `00b2a6a72646`
- **Références sortantes (7) :**
  - ❓ `import_module` → `sys` *(l.9)*
  - ❓ `import_module` → `asyncio` *(l.11)*
  - ❓ `import_module` → `pathlib` *(l.12)*
  - ❓ `import_module` → `memory.memoire_conceptuelle` *(l.28)*
  - ❓ `import_module` → `memory.memoire_technique` *(l.34)*
  - ❓ `import_module` → `memory.gestionnaire_erreurs` *(l.41)*
  - ✅ `import_module` → `agent-multiloop-Gabriel-local\src\core\integrateur_memoire.py` *(l.51)*

### `tests\__init__.py`
- **Type :** python
- **Taille :** 0.0 o
- **Modifié :** 2026-08-03 14:07:48
- **Lignes :** 1
- **Hash MD5 :** `d41d8cd98f00`
- **Références sortantes :** *(aucune)*

### `tmp_geometrie_docx.zip`
- **Type :** autre
- **Taille :** 48.1 Ko
- **Modifié :** 2026-08-05 19:15:11
- **Hash MD5 :** `f25f387f67eb`
- **Références sortantes :** *(aucune)*
