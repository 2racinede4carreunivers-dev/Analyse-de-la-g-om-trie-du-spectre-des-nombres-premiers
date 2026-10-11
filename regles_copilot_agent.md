#  Règles Copilot Agent — Version optimisée pour le workflow de Philippe Savard

Ce document liste les règles recommandées pour limiter les requêtes coûteuses de GitHub Copilot Agent tout en préservant le bon fonctionnement du développement local (VS Code, pipelines PowerShell, Docker, Isabelle/HOL, théorie *L’univers est au carré*).

---

##  1. Limiter les révisions automatiques
- Désactiver les revues automatiques sur tous les dépôts.
- Autoriser uniquement les revues **manuelles**.
- Niveau d’effort : **Lite**.
- Désactiver les revues déclenchées par les bots.

**Impact :**  
Évite ~80 % des appels premium déclenchés automatiquement par GitHub.

---

##  2. Limiter les actions de l’agent sur les dépôts sensibles

Dépôts concernés :
- `univers_au_carre`
- `methode_spectral.thy`
- `orchestrator_main`
- `transmission_un_clic.py`
- Pipelines PowerShell (`*.ps1`)
- Dépôts HOL / Isabelle

Règles :
- Interdiction de création de branches par Copilot Agent.
- Interdiction de push automatique.
- Interdiction de commit automatique.
- Interdiction de modification de fichiers HOL.
- Interdiction de modification de fichiers `.thy`.
- Interdiction de modification de fichiers `.ps1`.
- Interdiction de modification de fichiers `.dockerfile`.
- Interdiction de modification de fichiers `.yml` (CI/CD).

**Impact :**  
Empêche Copilot d’altérer les dépôts mathématiques ou pipelines critiques, réduisant fortement les appels premium.

---

##  3. Limiter les actions de génération de fichiers
Copilot Agent peut générer :
- fichiers de tests,
- fichiers de documentation,
- fichiers de configuration.

Règles recommandées :
- Autoriser uniquement la génération de fichiers **Markdown**.
- Interdire la génération de fichiers **code source**.
- Interdire la génération de fichiers **config CI/CD**.
- Interdire la génération de fichiers **Docker**.
- Interdire la génération de fichiers **HOL / Isabelle**.

**Impact :**  
Réduction des appels premium d’un facteur ×10.

---

##  4. Limiter les actions de refactorisation
Règles recommandées :
- Autoriser uniquement les refactorings **manuels**.
- Interdire les refactorings automatiques.
- Interdire les refactorings multi-fichiers.
- Interdire les refactorings sur les dépôts mathématiques.

**Impact :**  
Évite les analyses profondes coûteuses.

---

##  5. Limiter les actions de sécurité
Règles recommandées :
- Désactiver les analyses de sécurité automatiques.
- Autoriser uniquement les analyses **manuelles**.
- Interdire les suggestions de patch automatique.

**Impact :**  
Évite les scans lourds (modèles reasoning ×13).

---

##  6. Limiter les actions de documentation
Copilot peut générer :
- README,
- documentation API,
- guides d’utilisation.

Règles recommandées :
- Autoriser uniquement la documentation **manuelle**.
- Interdire la documentation automatique sur les dépôts sensibles.
- Autoriser la documentation automatique uniquement sur les dépôts “sandbox”.

**Impact :**  
Réduit les appels premium de génération de texte long.

---

##  7. Limiter les actions de test
Règles recommandées :
- Interdire la génération automatique de tests.
- Autoriser uniquement la génération **manuelle**.
- Interdire les tests sur les dépôts HOL / Isabelle.

**Impact :**  
Évite les appels premium de génération de code.

---

##  8. Synthèse des règles globales recommandées
- **Aucune action automatique** (revue, génération, correction, refactorisation).
- **Aucune action multi-fichiers**.
- **Aucune action sur les dépôts mathématiques ou pipelines**.
- **Complétions de code VS Code illimitées** (sans impact).
- **Chat Copilot illimité** (sans impact).
- **PR manuelles uniquement**.
- **Contrôle total par le développeur**.

---

##  Notes pour le workflow de Philippe Savard
Ces règles sont optimisées pour :
- Développement d’agents logiciels multiloop.
- Dépôts GitHub liés à VS Code.
- Théorie personnelle *L’univers est au carré*.
- Dépôts HOL / Isabelle/HOL.
- Pipelines PowerShell et scripts Python.
- Environnements Docker orchestrés via `docker-compose`.

Elles minimisent la consommation de crédits Copilot tout en préservant la liberté de développement locale.

