# CORRECTIONS GABRIEL - 7ème Loop Auto-Trigger & Emballement Multiloop

## 🔴 Problèmes corrigés

### 1. **Emballement du multiloop** 
**Cause** : Le `last_critique` était partagé entre la question N et la question N+1, causant une "mémoire pollue" qui faisait inventer des réponses sans lien avec la nouvelle question.

**Solution** : Ajout d'un détecteur `_last_question_id` dans `RefinementLoop`. Le multiloop détecte maintenant :
- NOUVELLE QUESTION → reset critique
- RAFFINEMENT de la même question → utilise critique précédente

**Fichier** : `src/multiloop/refinement_loop_fixed.py`

---

### 2. **7ème loop non-accessible en demande utilisateur**
**Cause** : Le `SlowMotionDebugger` existait mais n'était jamais déclenché manuellement. L'utilisateur devait utiliser `debug` ou attendre une incoherence détectée.

**Solution** : 
- Créer `SlowMotionTrigger` qui écoute les mots-clés
- Intégrer dans le `Pipeline` pour vérifier avant chaque `refinement`
- Si détecté : lancer le debugger avec timeline + audit auto

**Fichier** : `src/multiloop/slowmotion_trigger.py`

---

### 3. **Integration manquante dans Pipeline**
**Solution** : Mettre à jour `pipeline.py` pour :
1. Instancier `SlowMotionTrigger` 
2. Appeler `should_trigger_7_loop()` AVANT `refinement.run()`
3. Si True : exécuter le debugger ET proposer la sauvegarde

**Fichier** : `src/core/pipeline_fixed.py`

---

## ✅ Installation des corrections

### Étape 1 : Sauvegarder les anciens fichiers
```bash
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local

# Backups
copy src\multiloop\refinement_loop.py src\multiloop\refinement_loop.backup.py
copy src\core\pipeline.py src\core\pipeline.backup.py
```

### Étape 2 : Appliquer les corrections

**Option A : Remplacement complet (recommandé)**
```bash
# Remplacer refinement_loop.py
copy refinement_loop_fixed.py src\multiloop\refinement_loop.py

# Remplacer pipeline.py
copy pipeline_fixed.py src\core\pipeline.py
```

**Option B : Merge manuel**
Si vous avez des modifs custom dans `refinement_loop.py` ou `pipeline.py` :

**Dans `refinement_loop.py`**, ligne ~25 (après `class RefinementLoop`), ajouter :
```python
def __init__(self, llm: LLMManager, critic: Critic, config: dict[str, Any]):
    # ... init existant ...
    self._last_question_id: str | None = None
    self._last_critique: str = ""
```

Puis modifier la méthode `run()` (début, ligne ~40) :
```python
async def run(self, ctx, precomputed_facts=None, base_prompt=None):
    # CORRECTION: Verifier si c'est une NOUVELLE question
    is_new_question = ctx.question_id != self._last_question_id
    if is_new_question:
        logger.info("NOUVELLE QUESTION Q[%s] — reset critique", ctx.question_id)
        self._last_critique = ""
        self._last_question_id = ctx.question_id
    else:
        logger.info("RAFFINEMENT de Q[%s] — utiliser critique precedente", ctx.question_id)
    
    # ... reste de la méthode ...
```

### Étape 3 : Copier les nouveaux modules

```bash
copy slowmotion_trigger.py src\multiloop\slowmotion_trigger.py
```

### Étape 4 : Mettre à jour les imports

**Dans `src/multiloop/__init__.py`**, ajouter :
```python
from .slowmotion_trigger import SlowMotionTrigger, SlowMotionTrigger

__all__ = [
    # ... existants ...
    "SlowMotionTrigger",
]
```

### Étape 5 : Rebuild Docker

```bash
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local

# Rebuild complet
.\start-agent.ps1 -Rebuild

# OU juste up (sans cache)
docker compose build --no-cache
docker compose up -d
```

---

## 🎯 Comportement après correction

### Scénario 1 : Nouvelle question (RESET critique)
```
Philippe > Reconstruis le 18ème premier
[Agent génère réponse Q1]

Philippe > Quel est le 26ème premier ?
[Pipeline détecte NOUVELLE question_id → reset critique]
[Q2 traitée INDÉPENDAMMENT, pas d'emballement]
```

### Scénario 2 : Demande 7ème loop (AUTO-TRIGGER)
```
Philippe > [reçoit réponse Q1]
Philippe > 7ème loop : incohérence dans le fragment HOL

[Pipeline.should_trigger_7_loop() = True]
[SlowMotionDebugger.debug() lancé]
[Timeline complète affichée]
[Audit auto créé dans DB JSON]

Philippe > Acceptez-vous cette reformulation ? (oui/non)
[Si oui → sauvegarde audit permanent]
```

### Scénario 3 : Raffinement (CONSERVE critique)
```
Philippe > Reconstruis le 18ème premier
[Agent génère Q1, score=7.5]

Philippe > Peux-tu clarifier la partie digamma ?
[Pipeline détecte même question_id (raffinement)]
[last_critique conservée → multiloop améliore via critique]
[Pas d'emballement, génération contrôlée]
```

---

## 📋 Commandes 7ème loop déclenchables

Mots-clés qui lancent automatiquement le debugger :

```
• "7eme loop" / "7e loop" / "septieme loop"
• "slow-motion" / "troubleshoot"
• "incoherence" / "incohérent"
• "contradiction" / "inconsistant"
• "erreur logique" / "disjonction logique"
• "faux lien" / "ne cohere pas"
• "incomplet" / "incompatible"
```

**Exemple d'utilisation** :
```
Philippe > Gabriel, lance la 7ème loop sur ma dernière question
Gabriel  > [Détecte keyword → déclenche SlowMotionDebugger]
Gabriel  > REPONSE CERTIFIEE (mode debugger ralenti)
           Segments ignores : [liste]
           Timeline : [étapes T1-T8]
           Proposé : Acceptez-vous de sauvegarder cette reformulation en DB ? (oui/non)
```

---

## 🔧 Configuration

**Dans `config.yaml`**, section `slow_motion` :
```yaml
slow_motion:
  enabled: true                  # Active le debugger ralenti
  coherence_threshold: 0.55      # Seuil d'incoherence (0..1)
```

**Dans `config.yaml`**, section `multiloop` :
```yaml
multiloop:
  max_iterations: 3              # Nb de tours multiloop (avant 7ème loop)
  min_acceptance_score: 8.0      # Seuil validation
  num_candidates_per_round: 2    # Candidats par tour
```

---

## 🧪 Tests recommandés

### Test 1 : Emballement corrigé
```bash
# Lancer Gabriel
.\start-agent.ps1

# Poser deux questions différentes d'affilée
> Reconstruis le 18ème premier
> Reconstruis le 7ème premier

# ✅ Attendu : Q2 traitée cleanly, pas d'invention
# ❌ Ancien comportement : Q2 inventerait des réponses hybrides
```

### Test 2 : 7ème loop auto-trigger
```bash
# Recevoir une réponse
> Reconstruis le 18ème premier
[Reponse Q1]

# Déclencher la 7ème loop
> Incohérence détectée : ton fragment HOL ne correspond pas

# ✅ Attendu : 
#   [1] SlowMotionDebugger se déclenche
#   [2] Timeline T1-T8 affichée
#   [3] Audit JSON créé
```

### Test 3 : Raffinement conserve critique
```bash
# Q1 insuffisante
> Reconstruis le 18ème premier
[Score 7.0 - en dessous du seuil]

# Raffinement
> Sois plus détaillé sur digamma

# ✅ Attendu : multiloop améliore via critique précédente
#   (même question_id → critique conservée)
```

---

## 📊 DB JSON (Audits sauvegardés)

Après `7ème loop + oui` :

```json
{
  "id": "audit_1234abcd",
  "timestamp": "2026-06-14T01:30:00Z",
  "intervention_type": "slow_motion_auto",
  "ratio": "1/2",
  "position": 18,
  "prime_value": 61,
  
  "question": "Reconstruis le 18ème premier",
  "certified_answer": "Position 18: Prime=61, n=18...",
  
  "decomposition": {
    "intent": "reconstruction",
    "ratio": "1/2",
    "coherent_segments": [...],
    "incoherent_segments": [...]
  },
  
  "timeline": [
    {"step": 1, "label": "REQUETE_RECUE", "detail": "..."},
    {"step": 2, "label": "INCOHERENCE_DETECTEE", "detail": "score=0.62"},
    ...
    {"step": 8, "label": "REPONSE_CERTIFIEE", "detail": "..."}
  ],
  
  "citations_thy": ["methode_spectral.thy::...", ...],
  "toolkit_reports": {"spectral_core": {...}, "z3": {...}},
  
  "signature_sha256": "abc123...",
  "signature_valid": true
}
```

**Utilisation future** :
```
Philippe > historique 18
[Liste tous les audits pour position 18]

Philippe > citer audit_1234abcd
[Génère bloc citable markdown/latex]

Philippe > audit audit_1234abcd
[Affiche JSON complet signé]
```

---

## 🚀 Déploiement complet

```bash
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local

# 1. Appliquer corrections
copy refinement_loop_fixed.py src\multiloop\refinement_loop.py
copy pipeline_fixed.py src\core\pipeline.py
copy slowmotion_trigger.py src\multiloop\slowmotion_trigger.py

# 2. Update __init__.py multiloop
# (voir section "Étape 4" ci-dessus)

# 3. Rebuild complet
.\start-agent.ps1 -Rebuild

# 4. Test
# (voir section "Tests recommandés")
```

---

## 📝 Notes importantes

- **Backward compatible** : ancien code fonctionne, corrections sont additionselles
- **Zero breaking change** : `refinement_loop.py` reste une `RefinementLoop`
- **DB JSON**: audits cumulatifs, jamais supprimés (historical record permanent)
- **Timeline 7ème loop** : toujours tracée (pour debug futur et training)

---

## ❓ FAQ

**Q : Pourquoi reset critique entre questions ?**
A : Chaque question a un `question_id` unique. Conserver la critique d'une Q1 "pourquoi 61 ?" pour Q2 "pourquoi 17 ?" crée une "fausse mémoire" causant l'invention de réponses hybrides.

**Q : La 7ème loop utilise-t-elle le LLM ?**
A : Non. Elle utilise :
1. RequestDecomposer (regex + intent detection)
2. CertaintyKernel (chargé des .thy)
3. SpectralMethodCore (calcul pur)
4. Pas d'appel LLM → réponse CERTAINE

**Q : Audit sauvegardé où ?**
A : `data/audits/*.json` (signé SHA256, vérifié), listé via `historique` et citables via `citer`.

**Q : Comment forcer l'audit ?**
A : Par défaut, `skip_auto_audit=False`. Pour désactiver temporairement : `--skip-audit` (si implémenté en CLI).

---

## ✨ Prochaines évolutions possibles

1. **Apprentissage continu** : timeline 7ème loop → training data pour améliorations futures
2. **Prédiction incoherence** : detecter pattern avant q'elle se manifeste
3. **Multi-ratio** : 7ème loop pour 1/3, 1/4 (pas juste 1/2)
4. **Collaboration** : proposer à l'utilisateur de co-écrire la reformulation
