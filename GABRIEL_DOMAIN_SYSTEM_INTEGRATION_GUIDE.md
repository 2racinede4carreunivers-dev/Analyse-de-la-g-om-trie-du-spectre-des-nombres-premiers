# GABRIEL DOMAIN SYSTEM — Integration Guide

## Résumé

Gabriel est réconfiguré comme **agent HYPER-SPÉCIALISÉ** strictement limité au domaine **"Univers est au carré"**.

### Domaines Autorisés (EXCLUSIFS)
1. ✅ **Géométrie du Spectre des Nombres Premiers** (IMPLÉMENTÉ)
2. ⏳ **Mécanique Harmonique du Chaos Discret** (FUTUR)
3. ⏳ **Postulat Univers est au Carré** (FUTUR)
4. ⏳ **Espace de Philippôt** (FUTUR)

### Types de Requêtes Acceptées (dans domaine autorisé)
- **TECHNICAL_HOL**: Requêtes technique HOL/Isabelle
- **SPECTRAL_CALCULATION**: Calculs numérique (RsP, SA, SB)
- **EPISTEMOLOGICAL**: Questions théoriques/philosophiques/ontologiques
- **META_VALIDATION**: Certification, archivage, validation
- **CONVERSATIONAL**: Dialogue contextualisé

### Requêtes Rejetées
❌ **Toute requête hors domaine "Univers est au carré"**
- Politique générale
- Divertissement généraliste
- Santé générale
- Code/Tech généraliste
- Autres sciences

---

## Fichiers Créés

### 1. `domain_classifier.py`
Classifieur d'intent et de domaine.

**Classes principales:**
- `Domain` (enum): GEOMETRIE_SPECTRE_PREMIERS, etc.
- `RequestIntent` (enum): TECHNICAL_HOL, SPECTRAL_CALCULATION, etc.
- `DomainClassifier`: Classifie requêtes utilisateur
- `validate_domain_request()`: Fonction utilitaire

**Usage:**
```python
from src.multiloop.domain_classifier import DomainClassifier, validate_domain_request

classifier = DomainClassifier()
domain, intent, confidence, reason = classifier.classify("Calculer RsP(5,7)")

# Levant exception si rejet:
try:
    domain, intent, conf = validate_domain_request(user_input)
except DomainValidationError as e:
    print(e)  # Message de rejet
```

### 2. `gabriel_domain_config.py`
Configuration centralisée de Gabriel.

**Éléments:**
- `GABRIEL_IDENTITY`: Nom, titre, mission
- `AUTHORIZED_DOMAINS`: Domaines avec statut (IMPLEMENTED/FUTURE)
- `ACCEPTED_REQUEST_TYPES`: Types d'intent acceptés
- `REJECTED_KEYWORDS`: Mots-clés de rejet
- `COHERENCE_THRESHOLDS`: Seuils par intent (0.33 pour théorique, 0.65 pour technique)
- `DEBUGGER_TRIGGER_CONDITIONS`: Conditions pour déclencher slow-motion
- `RESPONSE_ROUTING`: Pipeline de réponse par intent

### 3. `domain_gate.py`
Gate à injecter en T0 du multiloop (point d'entrée unique).

**Classes principales:**
- `DomainValidationResult` (dataclass): Résultat de validation
- `GabrielDomainValidator`: Validateur
- `DomainGate`: Gate pour multiloop
- `@inject_domain_gate_to_multiloop`: Décorateur

**Usage:**
```python
from src.multiloop.domain_gate import DomainGate, inject_domain_gate_to_multiloop

# Approche 1: Utilisation directe
gate = DomainGate()
proceed, context = gate.execute(user_input)
if not proceed:
    print(context["rejection_message"])
    return

# Approche 2: Décorateur (recommandé)
@inject_domain_gate_to_multiloop
def my_multiloop(user_input, **kwargs):
    # domain, intent, confidence sont dans kwargs
    domain = kwargs.get("domain")
    intent = kwargs.get("intent")
    ...
```

---

## Intégration dans Multiloop

### Étape 1: Importer la gate

```python
# Dans src/multiloop/__init__.py ou votre orchestrateur multiloop

from src.multiloop.domain_gate import (
    DomainGate, 
    inject_domain_gate_to_multiloop,
    initialize_gabriel_domain_system
)
from src.multiloop.gabriel_domain_config import COHERENCE_THRESHOLDS

# Initialiser au démarrage
validator = initialize_gabriel_domain_system()
```

### Étape 2: Injecter en T0

**Approche A: Décorateur (recommandé)**
```python
@inject_domain_gate_to_multiloop
def gabriel_multiloop(user_input: str, **kwargs):
    """Multiloop principal avec domain gate injecté automatiquement."""
    
    domain = kwargs.get("domain")  # Récupéré depuis gate
    intent = kwargs.get("intent")
    confidence = kwargs.get("confidence")
    bypass_slowmotion = kwargs.get("bypass_slowmotion", False)
    
    # Si bypass_slowmotion=True -> NE PAS déclencher slow-motion debugger
    if bypass_slowmotion and intent in ["epistemological", "conversational"]:
        use_debugger = False
    else:
        use_debugger = True
    
    # T1: Decomposition...
    # T2: Verification...
    # ... (reste du multiloop)
```

**Approche B: Orchestrateur externe**
```python
def run_gabriel(user_input: str):
    """Orchestrateur avec validation externe."""
    
    gate = DomainGate()
    proceed, context = gate.execute(user_input)
    
    if not proceed:
        # Rejet immédiat
        return {
            "type": "DOMAIN_REJECTION",
            "response": context["rejection_message"],
        }
    
    # Acceptation: lancer multiloop avec contexte
    domain = context["domain"]
    intent = context["intent"]
    confidence = context["confidence"]
    bypass_slowmotion = context.get("bypass_slowmotion", False)
    
    return gabriel_multiloop(
        user_input,
        domain=domain,
        intent=intent,
        confidence=confidence,
        bypass_slowmotion=bypass_slowmotion,
        **context
    )
```

### Étape 3: Adapter Slow-Motion Debugger

**IMPORTANT**: Modifier `src/multiloop/slow_motion_debugger.py` pour respect les conditions:

```python
# Dans slow_motion_debugger.py

def should_trigger_slowmotion(
    multiloop_score: float,
    intent: str,
    domain: str,
    bypass_slowmotion: bool = False
) -> bool:
    """Décide si debugger doit se déclencher."""
    
    from gabriel_domain_config import DEBUGGER_TRIGGER_CONDITIONS, COHERENCE_THRESHOLDS
    
    # Bypass explicite du domaine
    if bypass_slowmotion:
        return False
    
    # Rejet au niveau domaine: TOUJOURS déclencher
    if domain == "out_of_domain":
        return True
    
    # Intent épistémologique: JAMAIS déclencher
    if intent in ["epistemological", "conversational"]:
        return False
    
    # Intent technique: déclencher si score < seuil
    threshold = COHERENCE_THRESHOLDS.get(intent, 0.50)
    if multiloop_score < threshold:
        return True
    
    return False
```

### Étape 4: Adapter les seuils de cohérence

**IMPORTANT**: Modifier les règles de cohérence pour respecter les seuils par intent:

```python
# Dans src/multiloop/coherence_detector.py

from gabriel_domain_config import COHERENCE_THRESHOLDS

def check_coherence(
    multiloop_score: float,
    intent: str,
    domain: str
) -> bool:
    """Vérifie cohérence avec seuils intent-aware."""
    
    if domain == "out_of_domain":
        return False  # Toujours rejet
    
    threshold = COHERENCE_THRESHOLDS.get(intent, 0.50)
    
    return multiloop_score >= threshold
```

---

## Architecture Complète (T0 à T11)

```
T0  [DOMAIN_GATE] ← Entrée unique
    |-> validate_domain_request()
    |-> Classification: domain + intent
    |-> Si rejet: STOP + rejection_message
    |-> Si acceptation: context enrichi

T1  [REQUEST_DECOMPOSITION]
    |-> context["domain"] utilisé pour router vers bon kernel

T2  [COHERENCE_CHECK]
    |-> Seuil adapté à context["intent"]
    |-> Pas de false positif sur théorique/conversationnel

T3  [SLOWMOTION_TRIGGER]
    |-> context["bypass_slowmotion"] respecté
    |-> NE PAS déclencher sur epistemological/conversational

T4-T10 [MULTILOOP_CORE]
    |-> Router vers pipeline approprié (TECHNICAL_HOL, SPECTRAL_CALC, etc.)

T11 [FINAL_RESPONSE]
    |-> Signature: FORMAL_HOL_RESPONSE | NUMERIC_SPECTRAL_RESPONSE | THEORETICAL_RESPONSE
```

---

## Comportement Attendu

### Test 1: Requête Technique HOL
```
INPUT: "Vérifier le lemme RsP_un_demi_general pour n1=5, n2=7"
DOMAIN_GATE: ✓ ACCEPT (domain=geometrie_spectre, intent=technical_hol)
SLOWMOTION: NE DECLENCHE PAS (intent technique, score sera bon)
MULTILOOP: FORMAL_HOL_RESPONSE
```

### Test 2: Requête Epistemologique (AVANT BUG)
```
INPUT: "Pourquoi 1/2 est un invariant central de la méthode spectrale?"
DOMAIN_GATE: ✓ ACCEPT (domain=geometrie_spectre, intent=epistemological)
SLOWMOTION: NE DECLENCHE JAMAIS (intent=epistemological -> bypass)
MULTILOOP: THEORETICAL_RESPONSE (pas de debugger)
```

### Test 3: Requête Méthodologique (ANCIEN BUG FIXE)
```
INPUT: "Je voudrais archiver mes résultats comme référence certifiée..."
DOMAIN_GATE: ✓ ACCEPT (domain=geometrie_spectre, intent=meta_validation)
SLOWMOTION: PEUT déclencher mais ne doit pas bloquer (seuil=0.50)
MULTILOOP: ARCHIVAL_DESIGN_RESPONSE
```

### Test 4: Requête Hors Domaine
```
INPUT: "Comment faire un gâteau?"
DOMAIN_GATE: ❌ REJECT (domain=out_of_domain)
SLOWMOTION: N/A
RESPONSE: "REJET: Requête hors domaine 'Univers est au carré'..."
```

---

## Fichiers à Modifier (Existants)

| Fichier | Modification | Priorité |
|---------|--------------|----------|
| `slow_motion_debugger.py` | Adapter `should_trigger()` pour respecter `bypass_slowmotion` | 🔴 HAUTE |
| `coherence_detector.py` | Utiliser `COHERENCE_THRESHOLDS[intent]` | 🔴 HAUTE |
| `request_decomposer.py` | Router vers kernel spectral basé sur `domain` | 🟡 MOYENNE |
| `verification_loop.py` | Adapter citations vers domaine spécialisé | 🟡 MOYENNE |
| Main orchestrateur | Injecter `@inject_domain_gate_to_multiloop` | 🔴 HAUTE |

---

## Tests

Exécuter:
```bash
cd src/multiloop
python domain_gate.py  # Tests unitaires
```

Résultat attendu:
```
✓ Input: Calculer RsP(5,7)
  Domain=geometrie_spectre_premiers Intent=spectral_calculation Valid=True

✓ Input: Pourquoi 1/2 est un invariant?
  Domain=geometrie_spectre_premiers Intent=epistemological Valid=True

✗ Input: Quel est le meilleur restaurant?
  Domain=out_of_domain Intent=out_of_domain Valid=False
```

---

## Résumé des Changements

| Aspect | Avant | Après | Impact |
|--------|-------|-------|--------|
| **Scope** | Monofonctionnel mais confus | HYPER-SPÉCIALISÉ | Clarté mission Gabriel |
| **Intent Classification** | Manquant | 6 classes + détection | Évite faux positifs |
| **Coherence Thresholds** | 0.50 unique | Adapté par intent (0.33-0.65) | Théorique pas sur-triggère |
| **Slowmotion Triggers** | Agressif | Intent-aware + bypass | Dialogue philosophique préservé |
| **Out-of-Domain Handling** | Confus | Rejet immédiat + message | Pas de "jouet" généraliste |
| **Domain Validation** | Implicite | Explicite en T0 | Sécurité++  |

---

## Prochaines Étapes

1. ✅ Modules créés: `domain_classifier.py`, `gabriel_domain_config.py`, `domain_gate.py`
2. 🔲 Modifier `slow_motion_debugger.py` pour `bypass_slowmotion`
3. 🔲 Modifier `coherence_detector.py` pour seuils intent-aware
4. 🔲 Tester avec rapport Gabriel d'hier (devrait passer sans debugger)
5. 🔲 Documenter cas d'usage pour Philippe

**Attends-tu que je modifie slow_motion_debugger.py maintenant ?**

# --- PIPELINE COGNITIF CONVOLUTIF ---
# Chargement dynamique de la base SQLite et regle de concisite multi-rapports
