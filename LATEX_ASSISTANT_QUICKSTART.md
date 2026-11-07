╔════════════════════════════════════════════════════════════════════════════╗
║      GABRIEL LaTeX ASSISTANT - QUICK START                                 ║
║                                                                            ║
║  Gabriel peut maintenant générer du LaTeX sans erreurs pour tes articles  ║
║  scientifiques sur la Méthode Spectrale!                                  ║
╚════════════════════════════════════════════════════════════════════════════╝

## FICHIERS CRÉÉS ✓

✓ src/core/latex_generator.py      (20.3 KB) - Moteur LaTeX
✓ src/ui/latex_commands.py         (9.6 KB)  - Intégration CLI

## INSTALLATION EN 3 ÉTAPES

### 1. Installer MikTeX (pour compiler PDF)

**Windows:**
- Télécharger: https://miktex.org/download
- Installer et redémarrer

**macOS:**
```bash
brew install mactex
```

**Linux:**
```bash
sudo apt install texlive-full
```

### 2. Vérifier installation

```bash
cd agent-multiloop-Gabriel-local
docker-compose build --no-cache
docker-compose up -d
docker-compose logs -f
```

### 3. Tester dans Gabriel

```bash
Gabriel > latex miktex-check
# Doit afficher: [✓ MikTeX DISPONIBLE]
```

═══════════════════════════════════════════════════════════════════════════

## COMMANDES PRINCIPALES

### Générer LaTeX pour tes 3 questions

```bash
# Q1: Rapport spectral 1×1
Gabriel > latex generate rsp1x1 2 3

# Q2: Reconstruction du 26e premier
Gabriel > latex generate reconstruction

# Q3: Écart spectral
Gabriel > latex generate gap -19 -5
```

### Valider (aucune erreur compilator)

```bash
Gabriel > latex validate "\documentclass{article}\begin{document}Test\end{document}"
# Résultat: [✓ VALIDE] ou [✗ ERREURS]
```

### Utiliser un template complet

```bash
Gabriel > latex template methode-spectrale
# Copier dans article_complet.tex
```

### Compiler en PDF

```bash
Gabriel > latex compile article_complet.tex
# Résultat: article_complet.pdf
```

═══════════════════════════════════════════════════════════════════════════

## WORKFLOW COMPLET

```
1. Générer contenu
   Gabriel > latex generate rsp1x1 2 3
   Gabriel > latex generate reconstruction 26 101
   Gabriel > latex generate gap -19 -5

2. Créer article.tex
   - Copier template methode-spectrale
   - Ajouter les sections générées

3. Valider syntaxe
   Gabriel > latex validate "<contenu article.tex>"
   # Résultat: [✓ VALIDE]

4. Compiler PDF
   Gabriel > latex compile article.tex
   # Résultat: article.pdf prêt!

5. Publier
   - ArXiV: https://arxiv.org
   - Journal académique
   - Conférence
```

═══════════════════════════════════════════════════════════════════════════

## EXEMPLES RAPIDES

### Créer article sur RsP

```bash
Gabriel > latex template methode-spectrale > article.tex
Gabriel > latex generate rsp1x1 7 11
# Copier output dans article.tex
Gabriel > latex validate "<contenu article.tex>"
Gabriel > latex compile article.tex
```

### Publier résultats

```bash
# Générer chaque question
Gabriel > latex generate reconstruction 50 229 >> article.tex
Gabriel > latex generate gap 101 113 >> article.tex

# Valider tout
Gabriel > latex validate "<contenu complet>"

# Compiler
Gabriel > latex compile article.tex
```

═══════════════════════════════════════════════════════════════════════════

## AVANTAGES

✓ **Pas d'erreurs LaTeX** - Gabriel valide automatiquement
✓ **Sections générées** - Q1, Q2, Q3 avec bonnes formules
✓ **Articles complets** - Templates scientifiques prêts
✓ **Compilations PDF** - Via MikTeX intégré
✓ **Pret à publier** - ArXiV, journals, conférences

═══════════════════════════════════════════════════════════════════════════

## PROCHAINES ÉTAPES

1. [ ] Installer MikTeX
2. [ ] Vérifier: `latex miktex-check`
3. [ ] Générer: `latex generate rsp1x1 2 3`
4. [ ] Créer: article.tex
5. [ ] Valider: `latex validate "<contenu>"`
6. [ ] Compiler: `latex compile article.tex`
7. [ ] Publier!

**Gabriel est maintenant un assistant LaTeX complet pour tes publications!** 📄✓
