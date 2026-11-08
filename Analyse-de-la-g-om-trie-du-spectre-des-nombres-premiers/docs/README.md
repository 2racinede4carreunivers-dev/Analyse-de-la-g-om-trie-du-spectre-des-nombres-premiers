# Site web du dépôt — Agent Multiloop Gabriel

Ce dossier `docs/` héberge la **page web publique** de présentation du dépôt.

## Activation sur GitHub Pages

1. Va dans **Settings → Pages** de ton dépôt GitHub.
2. Section *Build and deployment* :
   - **Source :** *Deploy from a branch*
   - **Branch :** `main`
   - **Folder :** `/docs`
3. Clique **Save**.
4. Après ~30 secondes, la page sera accessible sur :
   `https://2racinede4carreunivers-dev.github.io/agent-multiloop-Gabriel-local/`

## Fichiers

- `index.html` — page principale (HTML/CSS pur, aucune dépendance externe).
- `.nojekyll` — désactive le traitement Jekyll pour servir le HTML tel quel.

## Modifier la page

Édite simplement `index.html`. Le CSS est inline dans la balise `<style>` en tête du fichier. À chaque push sur `main`, GitHub Pages reconstruira automatiquement (~1 minute).

## Contact

Pour toute question ou modification structurelle :
📧 philipppthomassavard@gmail.com
