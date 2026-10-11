# Politique de Sécurité — Gabriel Multi-Loop

> 🇬🇧 An English version of this document is available: [`SECURITY.md`](./SECURITY.md)

**Auteur du projet :** Philippe Thomas Savard
**Dépôt :** `agent-multiloop-Gabriel-local`
**Dernière révision :** 25 juillet 2026
**Version couverte :** v3.35 → v3.38 et supérieures

---

## 1. Portée de cette politique

Ce document décrit la manière responsable de **signaler**, **traiter** et **divulguer** toute vulnérabilité de sécurité, faille logicielle ou anomalie de comportement affectant :

- Le code Python de l'agent (`src/`, `scripts/`, `tests/`)
- Les fichiers de théorie Isabelle/HOL (`theories/methode_spectral*.thy` et ses 7 traductions)
- Le conteneur Docker (`Dockerfile`, `docker-compose.yml`, `start-agent.ps1`)
- Les intégrations tierces (Anthropic Claude, OpenAI, Emergent Universal Key, Ollama)
- Les artefacts de preuve (audit trails JSON signés, PNG générés, RAG cognitif)
- La documentation publique (`README.md`, `docs/`, GitHub Pages)

---

## 2. Versions supportées

| Version | Support sécurité | Corrections actives |
|--------|:-:|:-:|
| v3.38.x (courante) | ✅ | ✅ |
| v3.37.x | ✅ | ✅ |
| v3.36.x | ✅ | Correctifs critiques uniquement |
| v3.35.x et antérieures | ⚠️ | Recommandation : migrer vers v3.38.x |

Les branches `stable` et `main` sont considérées comme officiellement supportées. Les autres branches (`Authentique-non-modifiable`, `Clonflit-*`, `conflict_*`, `secour`, `mise_jour_E1_*`) sont expérimentales et ne bénéficient d'aucun engagement de correctif.

---

## 3. Types d'anomalies acceptées

Nous acceptons les signalements pour :

### 3.1 Sécurité applicative
- Exécution de code non intentionnelle via une entrée utilisateur (CLI, RAG, prompt injection non filtré)
- Fuite d'une clé API (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `EMERGENT_LLM_KEY`) dans les logs, PNG, ou audit trails
- Contournement du `PreReasoner` permettant d'atteindre des LLM externes sans passer par les garde-fous
- Corruption ou falsification d'un `audit_trail_*.json` signé
- Contournement du `docker-compose` (élévation de privilèges, montage arbitraire de volumes)

### 3.2 Intégrité mathématique
- Résultat spectral incorrect ou reproduction numérique non-déterministe
- Divergence entre `theories/methode_spectral.thy` (source de vérité) et l'implémentation Python
- Régression de l'un des 1732 tests Pytest sans fix immédiat
- Incohérence entre les 8 versions linguistiques du `.thy` (le code HOL doit rester **identique bit-à-bit** entre FR/EN/ES/DE/PT/RU/ZH/JA)

### 3.3 Chaîne de compilation
- Échec de compilation Isabelle sur `main` (`isabelle build -D theories/` doit passer)
- Échec du workflow GitHub Actions `build.yml`
- Régression sur la génération d'images Docker (`docker compose build --no-cache`)

### 3.4 Confidentialité et conformité
- Fuite d'informations personnelles de l'auteur non prévues par le README
- Utilisation de code ou de bibliothèques violant les licences citées dans le README
- Attribution incorrecte de la Méthode Spectrale à un tiers

---

## 4. Comment signaler une anomalie

### 4.1 Canal privé (fortement recommandé pour les vulnérabilités critiques)

Envoyer un courriel à :

**`2racinede4carreunivers@gmail.com`**

Objet suggéré :
```
[SECURITE-GABRIEL] <catégorie> — <résumé en 5 mots>
```

Exemple :
```
[SECURITE-GABRIEL] Fuite clé — Universal Key visible dans logs Docker
```

### 4.2 Canal public (pour les anomalies non-critiques)

Ouvrir une *issue* GitHub :

**`https://github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local/issues/new`**

Utiliser le préfixe `[SECURITE]` dans le titre. **Ne jamais publier** de clé API, de token, ni de contenu extrait d'un `.env` dans une issue publique.

### 4.3 Informations à fournir dans le signalement

Pour accélérer le traitement, joindre :

- **Version affectée** (ex : `v3.38.1`, commit hash `6c0383f`)
- **Environnement** (OS, version Python, version Isabelle, version Docker)
- **Étapes de reproduction** minimales et déterministes
- **Comportement attendu** vs **comportement observé**
- **Logs pertinents** (extraits, pas fichiers complets — préalablement caviardés des clés API)
- **Impact perçu** (fuite, plantage, divergence mathématique, régression tests, etc.)
- **Preuve de concept** si applicable (script minimal reproduisant l'anomalie)

Un modèle de rapport est disponible dans `docs/security_report_template.md` (à créer si absent).

---

## 5. Engagement de traitement

| Étape | Délai indicatif |
|-------|:-:|
| Accusé de réception du signalement | Sous **72 heures ouvrables** |
| Triage initial et catégorisation | Sous **7 jours** |
| Correctif ou plan de mitigation | Selon la gravité (voir §6) |
| Publication du correctif sur `main` | Après validation par les 1732 pytests + `isabelle build` |
| Communication publique (si applicable) | Après le correctif, avec crédit au signalant |

---

## 6. Classification des gravités

| Niveau | Description | Objectif de correction |
|:-:|--------|:-:|
| **P0 — Critique** | Fuite de clé API, exécution de code arbitraire, corruption d'un `audit_trail` | ≤ 48 h |
| **P1 — Haute** | Régression mathématique majeure, échec de build Isabelle sur `main`, divergence entre versions linguistiques du `.thy` | ≤ 7 jours |
| **P2 — Moyenne** | Régression Pytest isolée, plantage CLI non exploitable, warning GitHub Actions | ≤ 30 jours |
| **P3 — Basse** | Faute de typographie, coquille dans un commentaire, amélioration cosmétique | Prochaine version mineure |

---

## 7. Politique de divulgation responsable

Nous demandons aux signalants de respecter les principes suivants :

1. **Confidentialité temporaire** : ne pas divulguer publiquement une vulnérabilité tant qu'un correctif n'est pas publié sur `main` ET disponible dans une image Docker publiée.
2. **Fenêtre d'embargo** : par défaut **90 jours** après réception du signalement, ou plus tôt si le correctif est publié.
3. **Absence d'exploitation** : ne pas exploiter la vulnérabilité au-delà du minimum nécessaire à sa démonstration.
4. **Pas de test destructif** : ne pas lancer d'attaque en déni de service, ni tenter d'accéder aux données d'autres utilisateurs.

En échange, nous nous engageons à :

- **Créditer le signalant** dans le CHANGELOG et la note de version, sauf demande d'anonymat.
- **Ne pas engager de poursuites** contre les chercheurs de bonne foi respectant cette politique.
- **Fournir un statut** à intervalles réguliers pendant l'investigation.

---

## 8. Zones hors périmètre

Les signalements suivants ne relèvent **pas** de cette politique de sécurité :

- Suggestions de fonctionnalités (utiliser une *feature request* GitHub classique)
- Bugs de comportement non-sécurité (utiliser une *bug report* GitHub classique)
- Débats sur la validité mathématique de la Méthode Spectrale (voir `theories/methode_spectral.thy` et publications associées)
- Comportements d'un LLM tiers (Claude, GPT) — ces éditeurs ont leurs propres canaux de signalement
- Problèmes affectant uniquement des versions non-supportées (voir §2)
- Vulnérabilités de dépendances tierces déjà connues et suivies dans `requirements.txt` — signaler plutôt à l'éditeur concerné

---

## 9. Attribution et remerciements

La liste des signalants ayant contribué à améliorer la sécurité de Gabriel Multi-Loop est maintenue dans le fichier `SECURITY_HALL_OF_FAME.md` (créé au premier signalement crédité).

---

## 10. Auteur, propriété intellectuelle et juridiction

- **Auteur unique** de la Méthode Spectrale et de son implémentation Gabriel Multi-Loop : **Philippe Thomas Savard**
- **Adresse** : Lévis, Chaudière-Appalaches, Québec, Canada
- **Juridiction applicable** aux litiges de sécurité : **droit québécois** et, subsidiairement, **droit canadien fédéral**
- **Licence du code source** : voir `LICENSE` à la racine du dépôt

---

## 11. Historique de révision

| Date | Version | Modification |
|------|---------|--------------|
| 2026-07-25 | 1.0 | Création initiale de la politique de sécurité |

---

## 12. Contact rapide

| Besoin | Canal |
|--------|-------|
| Vulnérabilité critique confidentielle | `2racinede4carreunivers@gmail.com` |
| Bug non-sécurité | GitHub Issues (préfixe `[BUG]`) |
| Question sur cette politique | GitHub Issues (préfixe `[SECURITE-QUESTION]`) |
| Contribution au correctif | Pull Request sur la branche `main` |

---

*Ce document est publié sous les mêmes termes que le code source du dépôt Gabriel Multi-Loop. Toute modification substantielle sera notée dans la section §11 « Historique de révision ».*
