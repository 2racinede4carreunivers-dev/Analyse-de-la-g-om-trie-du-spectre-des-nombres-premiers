# 🔐 SECURITY_GUIDE.md - Guide Sécurité Secrets & API Keys

## ⚠️ SITUATION ACTUELLE

**CRITIQUE**: Ton `.env` avec clé OpenAI est exposé sur GitHub!

**ACTIONS REQUISES MAINTENANT**:
1. Révoquer clé OpenAI compromise
2. Exécuter SECURITY_FIX.md (nettoyage git)
3. Appliquer nouveau .gitignore
4. Générer nouvelle clé OpenAI
5. Vérifier GitHub - aucun secret exposé

---

## 🚀 DÉMARRAGE RAPIDE - Nettoyage

```bash
# 1. Révoquer clé (IMMÉDIAT)
# → https://platform.openai.com/api-keys → Delete

# 2. Nettoyer git
cd C:\agent-multiloop-Gabriel-local-final
git filter-branch --tree-filter 'rm -f .env' -- --all
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 3. Retirer du tracking
git rm --cached .env

# 4. Vérifier .gitignore
git add .gitignore
git status  # .env NE doit PAS apparaître

# 5. Commit
git commit -m "Security: Remove .env from history"

# 6. Vérifier avant push
python security_validator.py

# 7. Push (avec --force car historique rewritten)
git push origin main --force

# 8. Générer nouvelle clé
# → https://platform.openai.com/api-keys → Create
# → Mettre dans .env LOCAL

# 9. Vérifier GitHub
# → .env DISPARU? .gitignore PRÉSENT?
```

---

## 📂 FICHIERS CRÉÉS POUR SÉCURITÉ

### 1. `.gitignore` (Racine dépôt)
**Exclut ALL fichiers sensibles**:
- `.env` et variantes
- API keys, tokens, credentials
- Logs, caches (peuvent contenir secrets)
- Memory sensible

### 2. `.env.example`
**Template SANS secrets**:
- Copier à `.env` et remplir
- JAMAIS commiter la version remplie
- Documente TOUTES les variables requises

### 3. `SECURITY_FIX.md`
**Guide détaillé nettoyage**:
- 6 étapes précises
- Options alternatives
- Checklists
- Prévention future

### 4. `security_validator.py`
**Script validation**:
- À exécuter AVANT `git push`
- Vérifie aucun secret dans staging
- Valide .gitignore
- Détecte patterns dangereux

---

## ✅ CHECKLIST - AVANT CHAQUE PUSH

**OBLIGATOIRE**:

```bash
# 1. Vérifier staging
git diff --cached | grep -E "(sk-|ghp_|password|secret)"
# → Devrait retourner RIEN

# 2. Vérifier .env n'est pas stagé
git status | grep -i ".env"
# → Devrait retourner RIEN ou seulement "deleted: .env"

# 3. Exécuter validator
python security_validator.py
# → Devrait retourner: "✓ SÉCURITÉ OK - Safe to push"

# 4. Vérifier .gitignore présent
ls -la | grep gitignore
# → Devrait afficher .gitignore

# 5. Double-check avant push
git log -1 --stat
# → NE doit PAS contenir .env, secrets, etc.
```

**SI UN CHECK ÉCHOUE**: NE PAS PUSHER!
Consulter SECURITY_FIX.md et corriger d'abord.

---

## 🔑 GESTION CLÉS API

### OpenAI (Kritique - Coût $$)

**Créer clé**:
1. https://platform.openai.com/api-keys
2. "Create new secret key"
3. Copier immédiatement (pas rechowable après!)
4. Mettre UNIQUEMENT dans `.env` LOCAL

**Révoquer clé**:
1. https://platform.openai.com/api-keys
2. Trouver clé
3. Click "Delete"
4. Générer NOUVELLE clé

**Sécuriser**:
- ✓ Utiliser new key après révocation
- ✓ Ne JAMAIS partager
- ✓ Ne JAMAIS commiter
- ✓ Rotationner tous les 3 mois
- ✓ Monitorer usage (https://platform.openai.com/account/usage)

### GitHub Token (Accès dépôt)

**Si utilisé**:
1. https://github.com/settings/tokens
2. Utiliser "Personal Access Token" (pas mot de passe!)
3. Permissions: "repo" (minimum)
4. Copier dans `.env` LOCAL ONLY

**Révoquer**:
1. https://github.com/settings/tokens
2. Delete token

### Wolfram Alpha (Optionnel)

**Similaire à OpenAI**:
- Générer depuis developer.wolframalpha.com
- Mettre dans `.env` LOCAL
- Ne JAMAIS commiter
- Rotationner si exposé

---

## 🚨 PATTERNS DANGEREUX À DÉTECTER

Security validator cherche automatiquement:

```
❌ sk-[20+ caractères]          (OpenAI keys)
❌ ghp_[36 caractères]          (GitHub tokens)
❌ api_key = "..."              (Génériques)
❌ password = "..."             (Mots de passe)
❌ OPENAI_API_KEY=sk-           (Env vars)
❌ GITHUB_TOKEN=ghp_            (Env vars)
```

**Si détecté**: Script refuse push jusqu'à correction!

---

## 📋 .gitignore - Couvert

Fichier `.gitignore` à la racine exclut:

```
# Secrets
.env*                    # Tous les .env
*.key, *.pem            # Certificats
secrets/, credentials/  # Dossiers sensibles

# Credentials
API keys, tokens
GitHub secrets
WolframAlpha keys

# Logs & Cache (peuvent contenir secrets)
logs/, *.log
__pycache__/
.cache/

# Données sensibles
memory/user_data.json
data/results/

# Local only
*.local
*.private
```

**Vérifier**:
```bash
git check-ignore -v .env
# Devrait retourner: ".env .gitignore:X"
```

---

## 🔄 WORKFLOW SÉCURISÉ

### Quotidien (Local)

```bash
# 1. Travailler normalement
# (modifie .env, mets secrets, etc.)

# 2. Commit travail (jamais .env)
git add .
git status
# Vérifier .env n'est PAS staged

# 3. Commit
git commit -m "Feature: ..."

# 4. Avant push: Validation
python security_validator.py
# ✓ SÉCURITÉ OK?

# 5. Push si OK
git push origin main
```

### Si accidentellement commité .env

```bash
# 1. STOP - Ne pas pusher!

# 2. Undo dernier commit (garder changements)
git reset --soft HEAD~1

# 3. Retirer .env du staging
git reset HEAD .env

# 4. Commit sans .env
git commit -m "Feature: ... (removed .env)"

# 5. Valider avant push
python security_validator.py

# 6. Push
git push origin main
```

### Si DÉJÀ pushé vers GitHub

```bash
# 1. Révoquer clé OpenAI IMMÉDIATEMENT
# https://platform.openai.com/api-keys → Delete

# 2. Nettoyer historique (voir SECURITY_FIX.md)
git filter-branch --tree-filter 'rm -f .env' -- --all

# 3. Force push
git push origin main --force

# 4. Générer nouvelle clé OpenAI

# 5. Monitoriser pour abus
# https://platform.openai.com/account/usage
```

---

## 🛡️ PRÉVENTION

### Git Hooks (Automatique)

Créer `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Empêche commit avec secrets

patterns="sk-|ghp_|password|secret"

git diff --cached | grep -E "$patterns" && {
  echo "❌ ERROR: Secrets detected in commit!"
  echo "   Do not commit secrets to version control"
  exit 1
}

# Vérifier .env n'est pas stagé
git diff --cached --name-only | grep -E "^\.env$" && {
  echo "❌ ERROR: .env file about to be committed!"
  echo "   .env should NEVER be in version control"
  exit 1
}

exit 0
```

**Installer**:
```bash
chmod +x .git/hooks/pre-commit
```

### GitHub Settings (Protection)

1. Go to: Repo Settings → Security → Secret scanning
2. Enable "Push protection"
3. GitHub refusera les commits avec secrets!

### Monitoring

Vérifier régulièrement:

```bash
# Usage OpenAI
# https://platform.openai.com/account/usage

# GitHub token activity
# https://github.com/settings/security-log

# Docker registry (si utilisé)
# Check for exposed credentials
```

---

## 📞 EN CAS DE PROBLÈME

### Clé exposée

```
1. Révoquer IMMÉDIATEMENT
2. Générer nouvelle clé
3. Mettre à jour .env
4. Rechercher usages (grep -r)
5. Changer partout où utilisée
```

### .env toujours visible sur GitHub

```
1. Vérifier git push --force a bien exécuté
2. Attendre cache GitHub à se clearer (24h)
3. Vérifier: curl https://api.github.com/.../contents/.env
   → Devrait retourner 404
4. Refaire filter-branch si persiste
```

### Impossible retirer .env de l'historique

```
1. Télécharger tous fichiers SAUF .env
2. Créer nouveau dépôt vide
3. Git init + push sans histoire
4. Delete ancien dépôt
5. Utiliser nouveau
```

---

## ✅ FINAL CHECKLIST

AVANT de pousser vers GitHub publiquement:

- [ ] `.gitignore` créé et en place
- [ ] `.env.example` créé (template)
- [ ] `.env` LOCAL avec vraies valeurs
- [ ] `.env` N'EST PAS stagé
- [ ] `security_validator.py` exécuté ✓
- [ ] Historique Git nettoyé (filter-branch si nécessaire)
- [ ] Nouvelle clé OpenAI générée (l'ancienne révoquée)
- [ ] `git status` ne montre pas `.env`
- [ ] `git diff --cached` ne contient aucun secret
- [ ] GitHub Settings → Secret scanning = ON
- [ ] Pre-commit hook installé (optionnel mais recommandé)
- [ ] Dernière vérification: `python security_validator.py`

**SI TOUT ✓**: Safe to push!

---

## 📚 RESSOURCES

- `.gitignore` - Fichier d'exclusion
- `.env.example` - Template variables
- `SECURITY_FIX.md` - Nettoyage détaillé
- `security_validator.py` - Validation automatique
- `.git/hooks/pre-commit` - Protection locale

---

**Statut**: 🔴 URGENT - À TRAITER IMMÉDIATEMENT
**Document**: SECURITY_GUIDE.md
**Version**: 1.0

**Ne PAS pusher vers GitHub tant que problème n'est pas résolu!**
