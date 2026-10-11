# DOCUMENT UNIQUE DESTINÉ À E1 — Multi-Loop Agent (Architecture + Runtime + Déploiement)

## 1. 🎯 Objectif du Système

Agent mathématique capable d'abstraction, d'inférence, de généralisation et de découverte,
basé sur la Méthode Spectrale de Philippe Thomas Savard (rapports 1/2, 1/3, 1/4)
et utilisant Isabelle/HOL pour la validation formelle.

## 2. 🧠 Les 5 Moteurs Cognitifs

### 2.1 Moteur d'Abstraction (engines/abstraction/)
- abstraction_layer.py, concept_extractor.py, abstraction_rules.py
- Transforme une question spécifique en pattern conceptuel réutilisable.

### 2.2 Moteur de Généralisation (engines/generalization/)
- generalizer.py, pattern_matcher.py, generalization_rules.py
- Transforme une solution spécifique en template général.

### 2.3 Moteur de Méta-raisonnement (engines/meta_reasoning/)
- proof_planner.py, goal_analyzer.py, strategy_selector.py
- Orchestre les moteurs, sélectionne les stratégies.

### 2.4 Moteur de Découverte de Théorèmes (engines/theorem_discovery/)
- discovery_loop.py, conjecture_generator.py, conjecture_filter.py
- Génère, filtre et valide des conjectures.

### 2.5 Moteur de Navigation Conceptuelle (engines/concept_navigation/)
- graph_builder.py, navigator.py, query_mapper.py
- Navigue dans un graphe de concepts.

## 3. 🏗️ Architecture Globale

```
UI / CLI
    ↓
Pipeline Multi-Boucles (core/pipeline.py)
    ↓
Planner (core/planner.py)
    ↓
5 Moteurs Cognitifs
    ↓
HOL/Isabelle (adapters/hol_isabelle/)
    ↓
Réponse
```

## 4. 📁 Structure

```
multi_loop_agent/
├── core/              # Cœur du système
├── engines/           # 5 moteurs spécialisés
├── adapters/          # Connecteurs (Isabelle, corpus, QA, LLM)
├── ui/                # Interfaces (CLI, API)
├── tests/             # Tests unitaires
├── scripts/           # Scripts utilitaires
├── configs/           # Configuration YAML
├── data/              # Corpus, QA bank, index
├── theories/          # Fichiers .thy (HOL)
└── logs/              # Journaux
```

## 5. 🔄 Pipeline Cognitif

1. Abstraction
2. Méta-raisonnement
3. Navigation conceptuelle
4. Généralisation
5. Découverte (optionnel)
6. Génération script HOL
7. Validation Isabelle
8. Réponse utilisateur

## 6. 🐳 Runtime
- Docker Desktop
- docker-compose : services math-agent-cli, llm-agent-multiloop, ollama, ollama-init, isabelle
- Volume `./theories:/theories` pour les fichiers .thy
- LLM : OpenAI (clé utilisateur) avec fallback Ollama (llama3.2)

## 7. 🎯 Domaines mathématiques couverts (du corpus)
- Méthode Spectrale de Philippe Thomas Savard
- Rapport spectral 1/2, 1/3, 1/4 (positifs et négatifs)
- Suites SA, SB, A_1_3, B_1_3, A_1_4, B_1_4
- Digamma calculé, équations de premier
- Suites mixtes (-,+)
- Géométrie spectrale, asymétrie ordonnée/chaotique
- Plan trifocal (FZg, HyRi, MsP), validation épipolaire
- Lien avec fonction zêta de Riemann, hypothèse de Riemann
- Isabelle/HOL, preuves formelles
