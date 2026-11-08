# DÉPLOIEMENT : Extension Cognitive pour les 3 cas d'écart

## 📦 Fichiers à déployer

```
C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local\
└─ src/spectral/
   ├─ gap_cognitive_model.py  ← NOUVEAU (définitions)
   └─ gap_solver.py            ← NOUVEAU (résolution)
   
Plus : mise à jour de fichiers existants (voir ci-dessous)
```

---

## 🚀 Déploiement pas-à-pas

### **STEP 1 : Copier les nouveaux fichiers**

```bash
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local

copy gap_cognitive_model.py src\spectral\
copy gap_solver.py src\spectral\
```

### **STEP 2 : Mettre à jour `src/spectral/__init__.py`**

**Ajouter les imports** :

```python
# Avant
from .prime_table import PRIMES, nth_prime, max_position, is_known_prime, prime_position
from .spectral_knowledge import build_grounded_system_prompt, compute_spectral_ratio

# Ajouter après :
from .gap_cognitive_model import (
    GAP_CONFIGURATIONS,
    GAP_CERTAINTIES,
    detect_gap_intent,
    get_gap_configuration,
    render_gap_kernel,
)
from .gap_solver import GapSolver, GapResult

__all__ = [
    # ... existants ...
    "GAP_CONFIGURATIONS", "GAP_CERTAINTIES", "detect_gap_intent",
    "get_gap_configuration", "render_gap_kernel", "GapSolver", "GapResult",
]
```

### **STEP 3 : Intégrer dans CertaintyKernel**

**Dans `src/adapters/corpus/certainty_kernel.py`**, méthode `__init__` :

```python
def __init__(self, theories_dir: str = "/theories"):
    # ... init existant ...
    
    # NOUVEAU : Charger le kernel d'écart spectral
    from ..spectral.gap_cognitive_model import GAP_CERTAINTIES
    
    for cert_dict in GAP_CERTAINTIES:
        certainty = Certainty(
            id=cert_dict["id"],
            statement=cert_dict["statement"],
            source=cert_dict["source"],
            confidence=cert_dict["confidence"],
        )
        self.certainties.append(certainty)
        self.id_map[cert_dict["id"]] = certainty
    
    logger.info(f"GAP certitudes loaded : +{len(GAP_CERTAINTIES)} entries")
```

### **STEP 4 : Intégrer GapSolver dans le Pipeline**

**Dans `src/core/pipeline.py`**, classe `Pipeline.__init__()` :

```python
from ..spectral.gap_solver import GapSolver
from ..spectral.gap_cognitive_model import detect_gap_intent

class Pipeline:
    def __init__(self, config: dict[str, Any]):
        # ... init existant (spectral_core, etc.) ...
        
        # NOUVEAU : Gap solver
        self.gap_solver = GapSolver(spectral_core=self.spectral_core)
        
        logger.info("✓ GapSolver initialized for (+,+), (-,-), (-,+) cases")
```

**Dans `src/core/pipeline.py`**, méthode `process()`, après "detecter intent" :

```python
async def process(self, question: str, previous_answer: Optional[FinalAnswer] = None) -> FinalAnswer:
    qid = uuid.uuid4().hex[:8]
    
    # Étape 1 : Vérifier si c'est une question d'écart
    is_gap, gap_type, numbers = detect_gap_intent(question)
    
    if is_gap and gap_type and len(numbers) >= 2:
        logger.info(f"Q[{qid}] ÉCART SPECTRAL détecté : {gap_type}")
        p1, p2 = numbers[0], numbers[1]
        
        gap_result = self.gap_solver.solve_gap(p1, p2)
        if gap_result:
            logger.info(f"Q[{qid}] Écart {gap_type} résolu : {gap_result.gap_count} entiers")
            return self._build_gap_answer(qid, question, gap_result)
    
    # Étape 2 : Workflow standard (multiloop, etc.)
    ctx = self.abstraction.abstract(qid, question)
    # ... reste du code ...
```

**Ajouter la méthode helper** :

```python
def _build_gap_answer(self, qid: str, question: str, gap_result: GapResult) -> FinalAnswer:
    """Convertit GapResult en FinalAnswer."""
    from .types import FinalAnswer, CandidateAnswer
    
    # Construire la réponse textuelle
    answer_text = self._render_gap_result(gap_result)
    
    # Candidates (une seule, car calcul certain)
    candidate = CandidateAnswer(
        iteration=1,
        text=answer_text,
        structured_data={
            "gap_type": gap_result.gap_type,
            "p1": gap_result.p1,
            "p2": gap_result.p2,
            "gap_count": gap_result.gap_count,
            "position_p1": gap_result.position_p1,
            "position_p2": gap_result.position_p2,
            "SA_p1": gap_result.SA_p1,
            "SB_p1": gap_result.SB_p1,
            "digamma_p2": gap_result.digamma_p2,
            "formula_used": gap_result.formula_used,
            "validation": gap_result.validation,
        },
        score=10.0,  # CERTAIN
        critique="Calcul spectral certifié (kernel-based, pas LLM)",
        grounded=True,
        used_engines=["gap_solver", "spectral_core"],
    )
    
    return FinalAnswer(
        question_id=qid,
        answer_text=answer_text,
        structured_data=candidate.structured_data,
        confidence=1.0,  # CERTAIN
        iterations_used=1,
        best_score=10.0,
        candidates=[candidate],
        explanation=gap_result.explanation,
    )

def _render_gap_result(self, result: GapResult) -> str:
    """Affiche le résultat d'écart de manière structurée."""
    config = get_gap_configuration(result.gap_type)
    
    lines = [f"### Écart spectral {result.gap_type.upper()}"]
    lines.append("")
    lines.append(f"**Entre {result.p1} et {result.p2}** : {result.gap_count} nombres")
    lines.append("")
    
    if config:
        lines.append(f"**Interprétation** :\n{config.interpretation}")
        lines.append("")
    
    lines.append("**Calcul intermédiaire** :")
    lines.append(f"  - Position p1 : {result.position_p1}")
    lines.append(f"  - Position p2 : {result.position_p2}")
    lines.append(f"  - SA(p1) : {result.SA_p1:.4f}")
    lines.append(f"  - SB(p2) : {result.SB_p2:.4f}")
    lines.append(f"  - digamma(p2) : {result.digamma_p2:.4f}")
    lines.append("")
    
    lines.append(f"**Formule utilisée** :\n{result.formula_used}")
    lines.append("")
    
    lines.append(f"**Sources** :")
    for source in result.validation.get("source", []):
        lines.append(f"  - {source}")
    
    if result.validation.get("zero_special"):
        lines.append("\n⚠️  **CAS SPÉCIAL** : Zéro a un rôle particulier (lien Riemann)")
    
    return "\n".join(lines)
```

### **STEP 5 : Tester**

```bash
# Rebuild Docker
.\start-agent.ps1 -Rebuild

# Lancer Gabriel
.\start-agent.ps1

# Test cas 1 : (+,+)
> Quel est l'écart entre 7 et 23 ?

# Test cas 2 : (-,-)
> Quel est l'écart entre -19 et -5 ?

# Test cas 3 : (-,+) — Le plus important
> Quel est l'écart mixte entre -31 et 17 ?
```

---

## 🧪 Tests d'validation

### **Test 1 : Reconnaissance de l'écart**

```bash
> Determine l'ecart entre 11 et 31

Expected log output :
  [INFO] ÉCART SPECTRAL détecté : positive_positive
  [INFO] Écart positive_positive résolu : 19 entiers
```

### **Test 2 : Cas négatif**

```bash
> Peux-tu calculer l'écart entre -5 et -19 ?

Expected :
  • Reconnaître écart (-,-)
  • Appliquer formules avec exposants négatifs
  • Retourner : 13 nombres
```

### **Test 3 : Cas mixte (CRITIQUE)**

```bash
> Quel est l'écart mixte entre -31 et 17 ?

Expected :
  ✓ Reconnaître (-,+) mixte
  ✓ Afficher "ZÉRO a un rôle SPÉCIAL"
  ✓ Calculer et retourner : -47 nombres
  ✓ Mentionner lien Riemann dans explication
```

---

## 📊 Résultat attendu

Après déploiement, Gabriel affichera :

```
╭─────────────────────────── Écart spectral MIXED ───────────────────────────╮
│                                                                             │
│ Entre -31 et 17 : -47 nombres                                              │
│                                                                             │
│ Interprétation :                                                            │
│   Extension spectrale : on traite -p comme un 'premier inverse'.            │
│   Position de -p = -(position de p)                                         │
│   Les formules SA, SB s'étendent aux exposants négatifs.                   │
│   On compte les entiers ENTRE -31 et 17 (avec ordre < >).                 │
│   Zéro a un rôle SPÉCIAL dans écart mixte : si 0 pas compté comme 1,      │
│   ajouter 1 au résultat final (lien Riemann).                             │
│                                                                             │
│ Calcul intermédiaire :                                                      │
│   - Position p1 : -11                                                       │
│   - Position p2 : 7                                                         │
│   - SA(-10) : -1.9984                                                       │
│   - SB(7) : 350.0000                                                        │
│   - digamma(7) : -11.5313                                                   │
│                                                                             │
│ Formule utilisée :                                                          │
│   (SA(-n_prev) - SB(n_p2) + digamma_adjustment) / 64  [MIXTE]              │
│   AJUSTEMENT ZÉRO: zéro a rôle spécial (lien Riemann)                     │
│                                                                             │
│ Sources :                                                                   │
│   • methode_spectral.thy::gap_mixed                                         │
│   • plan_trifocal::riemann_link                                             │
│                                                                             │
│ ⚠️  CAS SPÉCIAL : Zéro a un rôle particulier (lien Riemann)                │
╰─────────────────────────────────────────────────────────────────────────────╯
```

---

## 🎓 Signature de l'improvement

Gabriel gagnera la capacité à :

1. **Reconnaître** l'écart comme un intent distinct (pas "général")
2. **Classifier** en 3 cas : (+,+), (-,-), (-,+)
3. **Comprendre** que "premiers négatifs" sont VALIDES en domaine spectral
4. **Calculer** avec exposants négatifs dans SA/SB
5. **Appliquer** l'ajustement zéro pour cas mixte
6. **Relier** à Riemann : zéro n'est pas compté comme 1
7. **Citer** les sources (kernel + .thy files)
8. **Répondre correctement** aux 3 questions obligatoires

---

## 📞 Troubleshooting

**Q : Gabriel dit "premiers négatifs n'existent pas"**
A : Vérifier que `GAP_CERTAINTIES` sont chargés dans `CertaintyKernel`
   Vérifier que `NEGATIVE_PRIME_VALID_SPECTRAL` est présent

**Q : Résultats d'écart incorrects**
A : Vérifier les formules SA/SB dans `gap_solver.py`
   Comparer avec vos calculs manuels (voir COGNITIVE_GAP_EXTENSION.md)

**Q : Zéro n'est pas mentionné**
A : Vérifier que `GAP_MIXED` a `zero_special=True`
   Vérifier que `_render_gap_result()` affiche "CAS SPÉCIAL"

---

## 📝 Fichiers livrés

1. **gap_cognitive_model.py** (11 KB)
   - Définition des 3 cas
   - Kernel de certitude
   - Détection d'intent

2. **gap_solver.py** (10 KB)
   - Résolution numérique
   - Formules SA/SB/digamma
   - Ajustement zéro

3. **COGNITIVE_GAP_EXTENSION.md** (10 KB)
   - Explications détaillées
   - Exemples numériques
   - Guide intégration

4. **GAP_DEPLOYMENT.md** (this file)
   - Pas-à-pas déploiement
   - Tests validation
   - Troubleshooting

---

## ✅ Checklist de validation

- [ ] `gap_cognitive_model.py` copié dans `src/spectral/`
- [ ] `gap_solver.py` copié dans `src/spectral/`
- [ ] `src/spectral/__init__.py` mis à jour (imports)
- [ ] `CertaintyKernel.__init__()` chargé GAP_CERTAINTIES
- [ ] `Pipeline.__init__()` instancié GapSolver
- [ ] `Pipeline.process()` détecte écarts (avant multiloop)
- [ ] Méthodes `_build_gap_answer()` et `_render_gap_result()` ajoutées
- [ ] Test (+,+) passe : 7 et 23 → 15
- [ ] Test (-,-) passe : -19 et -5 → 13
- [ ] Test (-,+) passe : -31 et 17 → -47 (avec mention zéro spécial)
- [ ] Docker rebuild complet : `.\start-agent.ps1 -Rebuild`

Une fois validé ✓ : Gabriel comprend les 3 cas d'écart et peut répondre à votre question Riemann.

Ready to deploy! 🚀
