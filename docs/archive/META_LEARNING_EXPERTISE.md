# META-LEARNING : Expertise Algorithmique de Gabriel pour la 7ème Loop

## 🎯 Objectif

Gabriel n'archive pas juste **"la solution"** (reformulation) mais **"comment je me suis débrouillée"** — la **stratégie, les étapes, les décisions, les outils utilisés** pour déboguer le problème.

Cette expertise est ensuite réutilisée pour des problèmes **similaires futurs**.

---

## 📚 Architecture

```
SESSION SLOW-MOTION
    ↓
    ├─ Question posée : "Reconstruis le 18ème premier"
    ├─ Incoherence détectée : digamma_calc = 847998.0 vs 61.0
    ├─ Timeline exécuté : T1 (reçu) → T2 (incoherence) → ... → T8 (réponse)
    ├─ Toolkits utilisés : spectral_core, z3, sympy
    └─ Stratégie appliquée : by-pass 3 segments → reformulation canonique
    
    ↓ [USER ACCEPTE]
    ↓
DebugSessionRecord
    ├─ session_id: "dbg_a1b2c3d4"
    ├─ question_pattern: r"(\d+).*premier"  [pour matching futur]
    ├─ coherence_signature: {"type":"value_mismatch", "affected":["digamma_calc"]}
    ├─ timeline_steps: [T1, T2, ..., T8 avec DECISIONS]
    ├─ toolkit_usages: [spectral_core.reconstruct_prime_1_2(...)]
    ├─ reformulation_strategy: {segments_bypassed, canonical_form, key_insight}
    ├─ lessons_learned: ["invariant n=position (1/2)", "ne jamais LLM après slow-motion", ...]
    └─ confidence: 0.95
    
    ↓ [SAVE DB]
    ↓
ExpertiseLibrary (DB JSON)
    ├─ data/expertise/dbg_a1b2c3d4.json
    ├─ pattern_index: {"r'(\d+).*premier'": ["dbg_a1b2c3d4", "dbg_x8y9z0a1"]}
    └─ signature_index: {"c2e8f7a9": ["dbg_a1b2c3d4", ...]}

    ↓ [FUTURE QUESTION]
    ↓
NOUVELLE QUESTION : "Reconstruis le 26ème premier"
    ├─ Chercher dans ExpertiseLibrary :
    │   - Pattern match : r"(\d+).*premier" ✓
    │   - Trouver sessions similaires
    ├─ Récupérer stratégie de "dbg_a1b2c3d4"
    └─ APPLIQUER DIRECTEMENT (by-pass multiloop) ← ACCÉLÉRATION
```

---

## 📋 Composants clés

### 1. **DebugSessionRecord** (L'enregistrement d'une session)

```python
@dataclass
class DebugSessionRecord:
    session_id: str              # "dbg_a1b2c3d4"
    timestamp: str               # "2026-06-14T01:30:00Z"
    
    # QUESTION
    original_question: str       # "Reconstruis le 18ème premier"
    question_pattern: str        # r"(\d+).*premier" [REGEX]
    domain: str                  # "spectral_reconstruction"
    ratio_model: str             # "1/2"
    
    # INCOHERENCE
    coherence_signature: CoherenceSignature  # Type + sévérité
    coherence_score_before: float            # 0.62
    
    # PROCESSUS DEBUGGAGE
    timeline_steps: list[TimelineStep]       # T1-T8 + DECISIONS
    toolkit_usages: list[ToolkitUsage]       # spectral_core, z3, sympy
    reformulation_strategy: ReformulationStrategy  # Segments by-passed, insight clé
    
    # RESULTAT
    reformulated_question: str   # La version simplifiée
    final_answer: str            # Réponse certifiée
    coherence_score_after: 1.0   # CERTAIN (kernel-only)
    
    # META-LEARNING
    lessons_learned: list[str]   # Leçons réutilisables
    confidence: float            # 0.95 (haute car kernel)
```

### 2. **TimelineStep** (Chaque étape du debug)

```python
@dataclass
class TimelineStep:
    step: int              # 1..8
    label: str             # "DECOMPOSITION", "BYPASS_SEGMENTS", etc.
    detail: str            # "intent=reconstruction ratio=1/2 coherents=[...] incoherents=[...]"
    decision_taken: str    # "Décomposer en segments logiques"
    toolkit_used: Optional[ToolkitUsage]  # Si spectral_core utilisé à cette étape
```

### 3. **ReformulationStrategy** (La tactique appliquée)

```python
@dataclass
class ReformulationStrategy:
    segments_bypassed: list[str]         # ["HOL fragment", "narrative section"]
    canonical_form: str                   # "Reconstruire le 18-ème premier en rapport 1/2"
    decomposition_method: str             # "request_decomposer (regex+intent)"
    reconstruction_steps: list[str]       # [T1, T2, ..., T8]
    key_insight: str                      # "INVARIANT: position = n = num_terms"
```

### 4. **ExpertiseLibrary** (Index + DB)

```python
class ExpertiseLibrary:
    sessions: dict[str, DebugSessionRecord]           # En mémoire
    pattern_index: dict[regex, list[session_id]]      # Matching par pattern
    signature_index: dict[hash, list[session_id]]     # Matching par signature incoherence
    
    def find_similar_sessions(question, coherence_sig) → [DebugSessionRecord]
    def get_reformulation_strategy_for_pattern(question) → ReformulationStrategy
```

---

## 🔄 Workflow complet

### **Phase 1 : Enregistrement (après une 7ème loop réussie)**

```
Utilisateur : "Acceptez-vous cette reformulation ?"
Utilisateur : "OUI"

    ↓ SlowMotionRecorder.record_session()
    
    1. Extract pattern : r"(\d+).*premier"
    2. Build coherence_signature : {type:"value_mismatch", affected:["digamma_calc"]}
    3. Build timeline_steps : [T1, T2, ..., T8] avec DECISIONS
    4. Extract toolkit_usages : spectral_core.reconstruct_prime_1_2 executed
    5. Extract reformulation_strategy : {by-pass 3 segments, key_insight}
    6. Extract lessons : ["invariant n=position", "ne jamais LLM après", ...]
    
    ↓ Create DebugSessionRecord
    ↓ Add to ExpertiseLibrary
    ↓ Save to disk : data/expertise/dbg_a1b2c3d4.json
    
Résultat : Session archivée avec session_id = "dbg_a1b2c3d4"
```

### **Phase 2 : Réutilisation (nouvelle question similaire)**

```
Utilisateur : "Reconstruis le 26ème premier"

    ↓ Pipeline.process()
    ↓ MetaLearningManager.should_apply_previous_strategy(question) ?
    
    YES → ExpertiseLibrary.find_similar_sessions(question)
        ├─ Pattern match : r"(\d+).*premier" ✓ MATCH
        ├─ Find [dbg_a1b2c3d4, dbg_x8y9z0a1, ...]
        ├─ Return top-1 : dbg_a1b2c3d4 (confidence=0.95)
        └─ Get strategy : {canonical_form, key_insight, lessons}
    
    → Apply learned strategy DIRECTLY (by-pass multiloop)
    
    NO → Run standard multiloop (fallback)
```

### **Phase 3 : Accélération progressive**

```
Session 1 : "Reconstruis 18ème premier"
    Time : ~60s (full multiloop + slow-motion)
    Result : Archive expertise
    
Session 2 : "Reconstruis 26ème premier"
    Time : ~5s (apply learned strategy directly)
    Result : Check against expertise → augment confidence
    
Session 3 : "Reconstruis 52ème premier"
    Time : ~3s (apply learned strategy + cache hit)
    Confidence : now 0.98
```

---

## 💾 DB JSON Format

Chaque session sauvegardée en `data/expertise/dbg_a1b2c3d4.json` :

```json
{
  "session_id": "dbg_a1b2c3d4",
  "timestamp": "2026-06-14T01:30:00Z",
  "original_question": "Reconstruis le 18ème premier",
  "question_pattern": "(\\d+).*premier",
  "domain": "spectral_reconstruction",
  "ratio_model": "1/2",
  
  "coherence_signature": {
    "incoherence_type": "value_mismatch",
    "affected_concepts": ["digamma_calc", "prime_equation"],
    "severity": 0.38
  },
  "coherence_score_before": 0.62,
  
  "timeline_steps": [
    {
      "step": 1,
      "label": "REQUETE_RECUE",
      "detail": "Reconstruis le 18ème premier",
      "decision_taken": "Initialiser debugger"
    },
    {
      "step": 2,
      "label": "INCOHERENCE_DETECTEE",
      "detail": "score=0.62 signals=['value_mismatch']",
      "decision_taken": "Lancer slow-motion"
    },
    {
      "step": 3,
      "label": "DECOMPOSITION",
      "detail": "intent=reconstruction ratio=1/2 coherents=[...] incoherents=[...]",
      "decision_taken": "Décomposer en segments",
      "toolkit_used": null
    },
    {
      "step": 6,
      "label": "RESOLUTION_CERTIFIEE",
      "detail": "Using spectral_core",
      "decision_taken": "Résoudre via CertaintyKernel",
      "toolkit_used": {
        "toolkit_name": "spectral_core",
        "operation": "reconstruct_prime_1_2",
        "input_values": {"position": 18},
        "output_values": {"prime": 61, "n": 18},
        "success": true,
        "execution_time_ms": 2.5
      }
    }
  ],
  
  "reformulation_strategy": {
    "segments_bypassed": ["HOL fragment mismatch", "calcul intermediaire"],
    "canonical_form": "Reconstruire le 18-ème premier (rapport 1/2, n=18)",
    "decomposition_method": "request_decomposer (regex+intent)",
    "key_insight": "INVARIANT (ratio 1/2): position = n = number_of_terms = 18"
  },
  
  "reformulated_question": "Reconstruire le 18-ème nombre premier...",
  "final_answer": "Position 18: Prime=61, n=18, Terms=18\nINVARIANT (ratio 1/2): position = n = number_of_terms = 18\n...",
  "coherence_score_after": 1.0,
  
  "lessons_learned": [
    "Questions sur 'N-ème premier' → invariant n = position (1/2 uniquement)",
    "spectral_core fournit certitude absolue (préférer au LLM)",
    "Décomposer + by-pass incoherences + résoudre par kernel = certitude",
    "Ne JAMAIS relancer LLM après slow-motion (elle invente)"
  ],
  
  "confidence": 0.95
}
```

---

## 🛠️ Installation

### Étape 1 : Créer la structure de répertoires

```bash
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local

# Créer src/learning/
mkdir src\learning
```

### Étape 2 : Copier les fichiers

```bash
copy debugging_expertise.py src\learning\
copy slowmotion_recorder.py src\learning\
copy meta_learning_integration.py src\learning\
```

### Étape 3 : Mettre à jour `src/learning/__init__.py`

```python
"""Module learning : meta-learning et expertise."""
from .debugging_expertise import (
    ExpertiseLibrary,
    DebugSessionRecord,
    CoherenceSignature,
    ReformulationStrategy,
    TimelineStep,
    ToolkitUsage,
)
from .slowmotion_recorder import SlowMotionRecorder
from .meta_learning_integration import MetaLearningManager, PipelineWithMetaLearning

__all__ = [
    "ExpertiseLibrary",
    "DebugSessionRecord",
    "SlowMotionRecorder",
    "MetaLearningManager",
    "PipelineWithMetaLearning",
]
```

### Étape 4 : Intégrer dans Pipeline

**Dans `src/core/pipeline.py`**, après `__init__` du Pipeline :

```python
from ..learning.meta_learning_integration import MetaLearningManager

class Pipeline:
    def __init__(self, config):
        # ... init existant ...
        self.meta_learning = MetaLearningManager()
```

### Étape 5 : Adapter la CLI

**Dans `src/ui/cli.py`**, après slow-motion affichée :

```python
# Demander à l'utilisateur d'accepter la reformulation
console.print("\nAcceptez-vous cette reformulation pour enregistrement en DB expertise ? (oui/non/skip)")
user_response = console.input("[magenta]>[/magenta] ").strip().lower()

if user_response in {"oui", "yes", "o", "y"}:
    session_id = await orchestrator.pipeline.meta_learning.record_successful_debug_session(
        original_question=question,
        debugger_result=final_answer,
        coherence_report=coherence_report,
        decomposed=decomposed,
        timeline_events=timeline.to_dict(),
        toolkit_reports=result.structured_data.get("toolkit_reports"),
        user_validation=True,
    )
    console.print(f"\n[green]✓ Session enregistrée : {session_id}[/green]")
    console.print(f"[dim]Expertise pour 'pattern' réutilisable futuro[/dim]")
```

### Étape 6 : Rebuild Docker

```bash
.\start-agent.ps1 -Rebuild
```

---

## 🎮 Utilisation

### **Commande 1 : Afficher expertise accumulée**

```
Philippe > expertise
[Affiche]
  Total sessions : 3
  Patterns connus : 2 (reconstruction, ratio)
  Types incoherence : 1 (value_mismatch)
  Confidence moyenne : 0.94
  Domaines : [spectral_reconstruction, spectral_ratio]
```

### **Commande 2 : Afficher lessons learned**

```
Philippe > lessons 1/2
[Affiche]
  • Questions sur 'N-ème premier' → invariant n = position
  • spectral_core fournit certitude absolue
  • Décomposer + by-pass + kernel = certitude
  • Ne jamais LLM après slow-motion
```

### **Commande 3 : Historique des sessions meta-learning**

```
Philippe > sessions
[Affiche]
  dbg_a1b2c3d4  | 18ème premier     | conf=0.95 | 1/2 | 7 days ago
  dbg_x8y9z0a1  | 26ème premier     | conf=0.96 | 1/2 | 4 days ago
  ...
```

### **Commande 4 : Détail d'une session**

```
Philippe > session dbg_a1b2c3d4
[Affiche]
  Original question : "Reconstruis le 18ème premier"
  Incoherence type : value_mismatch (digamma_calc)
  Timeline : [T1 REÇU, T2 INCOHERENCE, T3 DECOMPOSITION, ..., T8 REPONSE]
  Key insight : "INVARIANT position=n=num_terms"
  Lessons : [3 leçons]
  Confidence : 0.95
```

---

## ✨ Avantages

| Aspect | Avant | Après |
|--------|-------|-------|
| **Première 7ème loop** | ~60s (full debug) | ~60s (identique) |
| **Deuxième question similaire** | ~60s (multiloop à nouveau) | ~5s (apply learned strategy) |
| **Troisième+ similaire** | ~60s chaque | ~3s chaque (cache) |
| **Expertise accumulée** | 0 | N sessions archivées |
| **Réutilisabilité** | Aucune | Pattern matching + lessons |
| **Confiance** | Baisse (hallucinations) | Augmente (kernel+expertise) |

---

## 🔮 Évolutions futures

1. **Probabilistic weighting** : Au lieu d'un pattern, utiliser probabilités pour score similarité
2. **Online learning** : Mettre à jour confidence après chaque utilisation
3. **Transfer learning** : Appliquer lessons d'un domaine à un autre (1/2 → 1/3)
4. **Collaborative learning** : Si plusieurs Gabriel tournent en réseau, partager expertise
5. **Explainability** : Générer rapport "pourquoi cette stratégie a marché" pour l'utilisateur

---

## 📊 Monitoring

**Métriques suivies** :

```
ExpertiseLibrary.export_summary() →
  {
    "total_sessions": 5,
    "patterns_known": 3,
    "incoherence_types": 2,
    "avg_confidence": 0.945,
    "most_common_pattern": "(\d+).*premier",
    "time_saved_minutes": 127,  # Estimation
  }
```

---

## 🚀 Déploiement complet

```bash
# 1. Copier les 3 fichiers
copy debugging_expertise.py src\learning\
copy slowmotion_recorder.py src\learning\
copy meta_learning_integration.py src\learning\

# 2. Update __init__.py
# (voir Étape 3 ci-dessus)

# 3. Adapter pipeline.py et cli.py
# (voir Étapes 4-5)

# 4. Rebuild
.\start-agent.ps1 -Rebuild

# 5. Test
> Reconstruis le 18ème premier
> [Reponse Q1]
> [7eme loop + OUI]
> [Session enregistrée]

> Reconstruis le 26ème premier
> [Reponse Q2 via learned strategy] ← PLUS RAPIDE
```

---

## 🎓 Résumé

Gabriel n'oublie plus jamais comment elle a résolu un problème. Chaque 7ème loop réussie devient une **compétence algorithmique permanente** que l'agent applique pour des problèmes similaires futurs — **plus rapide, plus certain, sans hallucination**.

C'est une **vraie meta-learning** : apprendre à apprendre.
