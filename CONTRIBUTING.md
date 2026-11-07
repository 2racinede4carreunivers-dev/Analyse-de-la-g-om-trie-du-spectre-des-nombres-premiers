# Contributing to Gabriel Multi-Loop

> 🇫🇷 Merci de contribuer à Gabriel Multi-Loop, l'agent d'assistance à la démonstration de la **Méthode Spectrale** de Philippe Thomas Savard.
>
> This document is intentionally written in French — Gabriel's canonical working language. Contributors are welcome to submit code, comments and commit messages in French **or** English.

**Auteur du projet :** Philippe Thomas Savard — Lévis, Chaudière-Appalaches, Canada
**Contact principal :** `2racinede4carreunivers@gmail.com`
**Dernière révision :** 25 juillet 2026

---

## Table des matières

1. [Philosophie du projet](#1-philosophie-du-projet)
2. [Types de contributions acceptées](#2-types-de-contributions-acceptées)
3. [Mise en place de l'environnement](#3-mise-en-place-de-lenvironnement)
4. [Workflow Git](#4-workflow-git)
5. [Contribuer au code Python](#5-contribuer-au-code-python)
6. [Contribuer aux preuves Isabelle/HOL](#6-contribuer-aux-preuves-isabellehol)
7. [Contribuer aux traductions du `.thy`](#7-contribuer-aux-traductions-du-thy)
8. [Contribuer aux tests](#8-contribuer-aux-tests)
9. [Contribuer à la documentation](#9-contribuer-à-la-documentation)
10. [Checklist avant de soumettre une Pull Request](#10-checklist-avant-de-soumettre-une-pull-request)
11. [Signalement de sécurité](#11-signalement-de-sécurité)
12. [Attribution](#12-attribution)

---

## 1. Philosophie du projet

Gabriel Multi-Loop est **plus qu'un agent LLM** : c'est un compagnon de démonstration mathématique. Trois principes gouvernent toute contribution :

- **Vérité mathématique d'abord** — Le fichier `theories/methode_spectral.thy` est la **source de vérité formelle**. Tout code Python doit être en accord avec les théorèmes prouvés dans ce fichier.
- **Reproductibilité totale** — Aucune fonction ne doit dépendre d'un état caché ou d'une source aléatoire non-graine. Les 1732 tests Pytest doivent tous passer.
- **Traçabilité** — Chaque preuve, chaque graphe généré, chaque décision de PreReasoner produit un artefact JSON signé (audit trail). Toute nouvelle fonctionnalité mathématique doit émettre un audit trail.

---

## 2. Types de contributions acceptées

### 2.1 Bienvenues
- ✅ Corrections de bugs Python ou Isabelle (avec test de non-régression obligatoire)
- ✅ Nouveaux régimes spectraux (`1/k` pour k ≥ 5, régime négatif étendu, etc.)
- ✅ Optimisations de performance sur les 1732 tests
- ✅ Améliorations UI/UX du CLI (Rich, cinematic display)
- ✅ Nouvelles preuves ou lemmes dans `methode_spectral.thy`
- ✅ Corrections ou améliorations des 7 traductions du `.thy`
- ✅ Nouveaux tests unitaires ou d'intégration
- ✅ Documentation, tutoriels, exemples pédagogiques

### 2.2 Requièrent une discussion préalable (ouvrir une *issue* d'abord)
- ⚠️ Ajout de nouvelles dépendances Python (`requirements.txt`)
- ⚠️ Modification du `Dockerfile` ou de `docker-compose.yml`
- ⚠️ Renommage de constantes/types Isabelle déjà utilisés (`SA`, `SB`, `A_suite_ZeroZeta`…)
- ⚠️ Modification du schéma des audit trails JSON
- ⚠️ Changement de la table `PRIMES` (1000 entrées, cross-vérifiée)
- ⚠️ Refonte d'un module core (`spectral_core.py`, `orchestrator.py`)

### 2.3 Refusées par principe
- ❌ Modification substantielle des théorèmes de la Section XIII sans justification formelle
- ❌ Suppression ou altération de la vision affirmative de l'Hypothèse de Riemann dans le `.thy`
- ❌ Ajout de code qui appelle un LLM sans passer par le `PreReasoner` ou hors des gardes-fous existants
- ❌ Contournement du système d'audit trail signé
- ❌ Contribution de code sous licence incompatible avec Apache-2.0/MIT

---

## 3. Mise en place de l'environnement

### 3.1 Environnement Python

```bash
git clone https://github.com/2racinede4carreunivers-dev/agent-multiloop-Gabriel-local.git
cd agent-multiloop-Gabriel-local
python -m venv .venv
source .venv/bin/activate       # Linux/Mac
# .venv\Scripts\activate        # Windows PowerShell
pip install -r requirements.txt
pytest -q                       # doit afficher "1732 passed"
```

### 3.2 Environnement Isabelle/HOL

- Version requise : **Isabelle 2025-2** (aligné avec `.github/workflows/build.yml`)
- Installation : [https://isabelle.in.tum.de/website-Isabelle2025-2/installation.html](https://isabelle.in.tum.de/website-Isabelle2025-2/installation.html)

```bash
cd theories
isabelle build -D .             # doit passer sans erreur
```

### 3.3 Environnement Docker (optionnel mais recommandé)

```bash
docker compose build --no-cache
docker compose up
```

### 3.4 Clés d'API

- Créer un fichier `.env` à la racine (jamais commité, voir `.gitignore`)
- Variables acceptées : `EMERGENT_LLM_KEY`, `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`
- Une clé Emergent Universal (`sk-emergent-...`) suffit pour Claude + OpenAI + Gemini via `emergentintegrations`

---

## 4. Workflow Git

### 4.1 Branches officielles

- **`main`** — branche stable, tous les tests passent, Isabelle build OK
- **`stable`** — branche de release taggée (futur, pipeline GHCR Docker à venir)
- **`mise_jour_E1_*`** — branches parallèles pour Philippe (fusion périodique avec `main`)

### 4.2 Créer une branche de contribution

```bash
git checkout main
git pull github main
git checkout -b feature/nom-court-explicite
# ou : bugfix/description-courte
# ou : docs/section-a-corriger
```

### 4.3 Convention de messages de commit

Format recommandé (français ou anglais, tolérant) :

```
<type>: <résumé impératif court>

<corps optionnel expliquant le POURQUOI, pas le comment>

Refs #<numero-issue-si-applicable>
```

Types acceptés : `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `math`, `isabelle`, `translate`, `chore`

Exemples :
```
feat: ajout commande CLI psi pour digamma pur d'Euler
fix: doublon SA/SB dans Section XI.A (conflit constante Isabelle)
isabelle: renommage A_suite -> A_suite_ZeroZeta + section XI.A
translate: mise à jour des 7 versions .thy après section XI.A
math: preuve du lemme somme_A_eq_SA (cohérence forme fermée)
```

---

## 5. Contribuer au code Python

### 5.1 Style

- Python 3.11+
- **PEP 8** respecté, largeur ligne 100 caractères
- Docstrings au format Google ou NumPy (français ou anglais)
- **Type hints obligatoires** pour toute nouvelle fonction publique
- Lint : `ruff check src/ tests/` doit passer sans erreur

### 5.2 Structure des modules

```
src/
├── core/              # Cœur mathématique (spectral_core.py, pipeline, etc.)
├── spectral/          # Ratios, courbes, digamma, RSP command
├── multiloop/         # Orchestration LLM (PreReasoner, domain gates)
├── engines/           # Moteurs cognitifs (7 engines)
├── visualization/     # Rendu PNG, ASCII, tables
├── ui/                # CLI Rich, cinematic display
└── memory/            # RAG cognitif, dictionnaires
```

**Nouveau module ?** Ouvre une issue avant, on discute de l'emplacement.

### 5.3 Test obligatoire

Toute nouvelle fonction publique **doit** être couverte par un test dans `tests/`.

```bash
pytest tests/test_nouvelle_fonction.py -v
pytest tests/ -q     # tous les 1732+ tests doivent passer
```

---

## 6. Contribuer aux preuves Isabelle/HOL

Le fichier `theories/methode_spectral.thy` est **la référence formelle du projet**. Il compile actuellement à zéro erreur avec Isabelle 2025-2.

### 6.1 Règles absolues

- 🔒 **Ne jamais** modifier les théorèmes prouvés existants sans justification écrite dans le commit
- 🔒 **Ne jamais** ajouter d'axiome ambiant qui pourrait rendre la théorie inconsistante
- 🔒 **Toujours** vérifier avec `isabelle build -D theories/` avant de commiter
- 🔒 **Toujours** encapsuler les hypothèses dans une `locale` ou un `axiomatization` clairement nommé
- 🔒 Le static-check (`tests/test_section_XI_XII_integration.py`) doit passer

### 6.2 Ajouter un nouveau lemme

1. Placer le lemme dans la Section thématique appropriée
2. Utiliser des noms explicites : `lemma nom_de_la_propriete_regime_1_k`
3. Fournir une preuve complète (`by`, `proof - ... qed`, ou `sledgehammer` puis extraction manuelle)
4. Ajouter un `text \<open>...\<close>` d'introduction expliquant l'intention mathématique
5. Vérifier que les 8 versions linguistiques du `.thy` restent synchronisables (voir §7)

### 6.3 Renommage d'une constante

Si tu renommes une `consts`, `definition`, ou `locale` :

1. Grep dans TOUT le fichier pour trouver les références
2. Mettre à jour tous les `unfolding <ancien_nom>_def` en `unfolding <nouveau_nom>_def`
3. Ajouter une note dans le CHANGELOG.md indiquant le renommage
4. **Propager le renommage dans les 7 traductions** (voir §7)

---

## 7. Contribuer aux traductions du `.thy`

Le projet maintient 8 versions du fichier `methode_spectral.thy` :

| Fichier | Langue |
|---------|--------|
| `methode_spectral.thy` | Français (référence) |
| `methode_spectral_en.thy` | English |
| `methode_spectral_es.thy` | Español |
| `methode_spectral_de.thy` | Deutsch |
| `methode_spectral_pt.thy` | Português |
| `methode_spectral_ru.thy` | Русский |
| `methode_spectral_zh.thy` | 中文 |
| `methode_spectral_ja.thy` | 日本語 |

### 7.1 Règle d'or de la traduction

**Le code HOL doit rester STRICTEMENT identique bit-à-bit entre les 8 versions.**

Seuls les éléments suivants sont traduits :
- Les commentaires `(* ... *)` (natural language uniquement)
- Les blocs Isabelle `text \<open>...\<close>` (natural language uniquement)
- L'entête metadata en haut de fichier (libellés Fichier/File/Datei…)

**Ne jamais traduire :**
- Les identifiants de fonctions (`RsP`, `SA`, `SB`, `digamma_calc`, `A_suite_ZeroZeta`…)
- Les noms de théorèmes, lemmes, définitions, locales
- Les formules mathématiques
- Les références bibliographiques (`pdf::page_26`, etc.)
- La transcription API/IPA de l'entête (garder la prononciation française)

### 7.2 Régénérer une traduction

Après toute modification du `.thy` français :

```bash
export EMERGENT_LLM_KEY=sk-emergent-...
python scripts/translate_thy.py en           # une langue
python scripts/translate_thy.py en es de     # plusieurs
python scripts/translate_thy.py              # les 7 langues
```

Le script utilise Claude Sonnet 4.6 via l'Emergent Universal Key, avec :
- Parser à balances équilibrées pour les `\<open>/\<close>` imbriqués
- Extraction JSON robuste en 3 stratégies
- Validateur structurel post-traduction (fallback FR si markers cassés)

### 7.3 Vérifier l'intégrité d'une traduction

Le code HOL doit rester identique :

```bash
python -c "
import re
def strip_all(c):
    m = re.match(r'\(\*.*?\*\)\s*', c, re.DOTALL); c = c[m.end():] if m else c
    c = re.sub(r'\(\*.*?\*\)', '', c, flags=re.DOTALL)
    import sys; sys.path.insert(0,'scripts')
    from translate_thy import _find_balanced_text_blocks
    for s,e in reversed(_find_balanced_text_blocks(c)): c = c[:s]+c[e:]
    return re.sub(r'\s+', ' ', c).strip()
fr = open('theories/methode_spectral.thy').read()
en = open('theories/methode_spectral_en.thy').read()
print('IDENTIQUE' if strip_all(fr)==strip_all(en) else 'DIVERGE')
"
```

---

## 8. Contribuer aux tests

### 8.1 Structure

```
tests/
├── test_<nom_module>.py           # tests unitaires
├── test_<feature>_v<version>.py    # tests de features versionnées
└── isabelle_static_check.py        # invoqué par test_section_XI_XII_integration.py
```

### 8.2 Nommage

- Fichier : `test_<snake_case>.py`
- Classe : `class Test<PascalCase>`
- Méthode : `def test_<what_it_verifies>(self, ...)`

### 8.3 Exécution

```bash
pytest tests/ -q                              # tout
pytest tests/test_digamma_pure_v338.py -v     # un fichier
pytest -k "digamma"                           # pattern
pytest --lf                                   # last failed
```

### 8.4 Baseline actuelle

**1732 tests doivent passer**, 8 sont volontairement `skipped` (dépendances externes non installées en CI).

---

## 9. Contribuer à la documentation

- `README.md` — page d'accueil GitHub, en français avec sections anglaises
- `README_MATHEMATICAL_v2.md` — introduction pédagogique aux 13 régimes
- `README_CINEMATIC_MODE.md` — guide utilisateur du mode cinéma
- `docs/index.html` — GitHub Pages (site public)
- `PRD.md` (dossier `memory/`) — Product Requirements Document, versions v3.15 → v3.38

**Toute nouvelle fonctionnalité doit ajouter une entrée au `CHANGELOG.md`.**

---

## 10. Checklist avant de soumettre une Pull Request

Avant d'ouvrir ta PR, vérifie que **tous** les points ci-dessous sont OK :

- [ ] Ma branche est à jour avec `main` (`git rebase github/main`)
- [ ] Les 1732+ tests Pytest passent (`pytest tests/ -q`)
- [ ] Le static-check Isabelle passe (`pytest tests/test_section_XI_XII_integration.py`)
- [ ] Si le `.thy` FR a été modifié, les 7 traductions sont soit régénérées, soit une note explicite l'indique
- [ ] Le lint Ruff passe (`ruff check src/ tests/`)
- [ ] J'ai ajouté au moins un test qui couvre ma modification
- [ ] J'ai mis à jour le `CHANGELOG.md` (section `[Unreleased]`)
- [ ] Je n'ai commité aucune clé d'API (grep sur `sk-`, `ANTHROPIC`, `OPENAI`)
- [ ] Le message de commit suit la convention de la §4.3
- [ ] La PR utilise le template `.github/PULL_REQUEST_TEMPLATE.md`

---

## 11. Signalement de sécurité

Pour signaler une **vulnérabilité de sécurité**, ne pas utiliser une PR ni une issue publique. Voir **[`SECURITY.md`](./SECURITY.md)** (English) ou **[`declaration_securite.md`](./declaration_securite.md)** (français) pour la procédure de signalement responsable.

Contact confidentiel : **`2racinede4carreunivers@gmail.com`**

---

## 12. Attribution

Toute contribution acceptée sera créditée dans le fichier **[`AUTHORS`](./AUTHORS)** à la racine du dépôt. Les contributeurs peuvent demander l'anonymat via un pseudonyme.

Merci d'aider à faire avancer la Méthode Spectrale ! 🎓
