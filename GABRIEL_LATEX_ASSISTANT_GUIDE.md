╔════════════════════════════════════════════════════════════════════════════╗
║    GABRIEL LATEX ASSISTANT - GUIDE COMPLET                                 ║
║                                                                            ║
║  Gabriel peut maintenant:                                                 ║
║  1. VALIDER syntaxe LaTeX (aucune erreur de compilation)                  ║
║  2. GÉNÉRER sections LaTeX pour les 3 questions                           ║
║  3. COMPILER en PDF via MikTeX                                            ║
║  4. CRÉER articles scientifiques complets                                 ║
╚════════════════════════════════════════════════════════════════════════════╝

## MODULES CRÉÉS

1. `src/core/latex_generator.py` (20.3 KB)
   - LaTeXValidator : validation sans erreurs
   - LaTeXCodeGenerator : génère sections pour Q1/Q2/Q3
   - LaTeXArticleGenerator : crée articles complets
   - MikTeXCompiler : interface avec MikTeX

2. `src/ui/latex_commands.py` (9.6 KB)
   - Intégration CLI
   - Gestion des commandes latex*

═══════════════════════════════════════════════════════════════════════════

## COMMANDES DISPONIBLES

### 1. VALIDER SYNTAXE LaTeX

```bash
Gabriel > latex validate "\documentclass{article}\begin{document}Test\end{document}"
```

Vérifie:
✓ Structure document/body
✓ Appariement accolades/crochets
✓ Environments \\begin{...}\\end{...}
✓ Commandes reconnues
✓ Paquets connus

Résultat: [✓ VALIDE] ou [✗ ERREURS + warnings]

### 2. GÉNÉRER CODE LaTeX

**Q1.a - Rapport spectral 1×1:**
```bash
Gabriel > latex generate rsp1x1 3 5
```

Génère section LaTeX avec:
- Ensemble A et B
- Définition du rapport spectral
- Calcul et résultat
- Propriété d'invariance

**Q2 - Reconstruction:**
```bash
Gabriel > latex generate reconstruction
```

Génère section avec:
- Position n et nombre premier attendu
- Algorithme (3 étapes)
- Formule mathématique
- Résultat reconstruit

**Q3 - Écart spectral:**
```bash
Gabriel > latex generate gap -19 -5
```

Génère section avec:
- Deux nombres premiers
- Type d'écart (+,+) / (-,-) / (-,+)
- Formule d'écart
- Implication Riemann

### 3. AFFICHER TEMPLATES

```bash
Gabriel > latex template methode-spectrale
```

Templates disponibles:
- methode-spectrale : article complet (10-15 pages)
- court : article court (5-7 pages)
- theoreme : théorème + preuve

### 4. COMPILER EN PDF

```bash
Gabriel > latex compile mon_article.tex
```

Compile via MikTeX vers PDF.

**Exigence:** MikTeX installé sur la machine.

### 5. VÉRIFIER MikTeX

```bash
Gabriel > latex miktex-check
```

Status:
✓ MikTeX disponible + chemin
✗ MikTeX introuvable → instructions installation

═══════════════════════════════════════════════════════════════════════════

## INSTALLATION & CONFIGURATION

### A. Installation de MikTeX

**Windows:**
1. Télécharger: https://miktex.org/download
2. Installer (ajout automatique au PATH)
3. Redémarrer Gabriel

**macOS:**
```bash
brew install mactex
# Ou complet:
brew install mactex-no-gui
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install texlive-full
```

**Linux (RedHat/Fedora):**
```bash
sudo dnf install texlive-scheme-full
```

### B. Vérification

```bash
Gabriel > latex miktex-check
```

Doit afficher: [✓ MikTeX DISPONIBLE]

### C. Alternative Docker

MikTeX n'est pas requis si tu compiles dans le container:

```bash
docker-compose exec llm-agent-multiloop-run \
  pdflatex -interaction=nonstopmode mon_article.tex
```

═══════════════════════════════════════════════════════════════════════════

## WORKFLOW COMPLET

### Étape 1: Générer contenu LaTeX

```bash
Gabriel > latex generate rsp1x1 2 3
Gabriel > latex generate reconstruction 26 101
Gabriel > latex generate gap -19 -5
```

Copier les outputs dans un fichier `mon_article.tex`

### Étape 2: Valider syntaxe

```bash
Gabriel > latex validate "<contenu du fichier>"
```

Résultat: [✓ VALIDE] → continuer
Résultat: [✗ ERREURS] → corriger et recommencer

### Étape 3: Compiler PDF

```bash
Gabriel > latex compile mon_article.tex
```

Résultat: [✓ PDF généré]

### Étape 4: Publier

Soumettre le PDF à:
- ArXiV: https://arxiv.org
- Journal académique
- Conférence

═══════════════════════════════════════════════════════════════════════════

## EXEMPLE: CRÉER UN ARTICLE COMPLET

### 1. Utiliser le template

```bash
Gabriel > latex template methode-spectrale
```

Copier le code complet dans `article_complet.tex`

### 2. Générer sections

```bash
Gabriel > latex generate rsp1x1 7 11
Gabriel > latex generate reconstruction 50 229
Gabriel > latex generate gap 101 113
```

Ajouter les sections au template (remplacer "% Insérer ici")

### 3. Valider

```bash
Gabriel > latex validate "<contenu article_complet.tex>"
```

### 4. Compiler

```bash
Gabriel > latex compile article_complet.tex
```

### 5. Résultat

Fichier `article_complet.pdf` prêt à publier!

═══════════════════════════════════════════════════════════════════════════

## VALIDATION LaTeX - DÉTAILS

Le validateur vérifie automatiquement:

✓ **Structure:**
  - \\documentclass{...} présent
  - \\begin{document} et \\end{document}

✓ **Paires:**
  - Accolades { } appariées
  - Crochets [ ] appariés
  - Environments \\begin{X}...\\end{X}

✓ **Commandes:**
  - \\cite{} avec argument
  - \\ref{} avec argument
  - Commandes custom bien définies

✓ **Paquets:**
  - amsmath, amssymb, amsthm, etc.
  - Avertit si paquet inconnu

Résultat:
- GREEN [✓ VALIDE] : Peut compiler sans erreur
- YELLOW [⚠ AVERTISSEMENTS] : Possible warning
- RED [✗ ERREURS] : Ne compilera pas

═══════════════════════════════════════════════════════════════════════════

## INTÉGRATION CONTINUE (GitHub Actions)

Optionnel: Compiler PDF automatiquement à chaque push

**Fichier: `.github/workflows/latex.yml`**

```yaml
name: Build LaTeX PDF

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Install texlive
        run: |
          sudo apt-get update
          sudo apt-get install -y texlive-latex-base \
            texlive-fonts-recommended texlive-latex-extra
      
      - name: Compile LaTeX
        run: pdflatex -interaction=nonstopmode article.tex
      
      - name: Upload PDF
        uses: actions/upload-artifact@v3
        with:
          name: pdf-artifact
          path: article.pdf
```

Chaque push compile automatiquement le PDF!

═══════════════════════════════════════════════════════════════════════════

## MEILLEURES PRATIQUES

### 1. Validation AVANT compilation

Toujours valider d'abord:
```bash
Gabriel > latex validate "<code>"  # ✓ VALIDE
Gabriel > latex compile article.tex # Compile
```

### 2. Templates pour cohérence

Utiliser les templates Gabriel pour style uniforme:
```bash
Gabriel > latex template methode-spectrale
```

### 3. Sections générées automatiquement

Pour chaque question, générer avec Gabriel:
```bash
Gabriel > latex generate rsp1x1 2 3
Gabriel > latex generate reconstruction 26 101
Gabriel > latex generate gap -19 -5
```

Pas d'erreurs LaTeX = garantie!

### 4. Versionning

```bash
git add article.tex
git commit -m "Add LaTeX article for Method X"
git push  # GitHub Actions compile automatiquement
```

═══════════════════════════════════════════════════════════════════════════

## DÉPANNAGE

### Q: "MikTeX not found" après installation

→ Redémarrer Gabriel ou le container Docker

### Q: Erreur "Package X not found"

→ Valider avec Gabriel: `latex validate "<code>"`
→ Gabriel suggère les paquets manquants

### Q: PDF ne se compile pas localement mais ok dans Docker

→ Utiliser Docker pour compiler: 
```bash
docker-compose exec llm-agent-multiloop-run \
  pdflatex article.tex
```

### Q: Besoin de génération plus avancée

→ Créer custom template + modifier LaTeXArticleGenerator
→ Soumettre PR ou demander amélioration

═══════════════════════════════════════════════════════════════════════════

## RÉSUMÉ

Gabriel est maintenant un **assistant LaTeX complet**:

✓ Valide syntaxe (aucune erreur garantie)
✓ Génère sections pour Méthode Spectrale
✓ Compile PDF via MikTeX
✓ Crée articles scientifiques complets
✓ Prêt pour ArXiV / publication académique

**Workflow:** Generate → Validate → Compile → Publish! 🎓📄
