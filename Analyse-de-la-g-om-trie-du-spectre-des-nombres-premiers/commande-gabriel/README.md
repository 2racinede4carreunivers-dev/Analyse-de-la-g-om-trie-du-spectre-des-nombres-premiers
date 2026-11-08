# 📘 Documentation des commandes Gabriel

Ce dossier contient la documentation utilisateur de l'agent Gabriel Multi-Loop.

## 📂 Contenu

| Fichier | Format | Usage recommandé |
|---|---|---|
| `COMMANDES.md` | Markdown | Documentation complète, lisible sur GitHub, dans VS Code ou tout viewer Markdown |
| `AIDE-MEMOIRE.txt` | Texte brut | À imprimer ou afficher à côté du terminal pendant que vous travaillez avec Gabriel |

## 🎯 Quel fichier consulter ?

- **Vous débutez** → ouvrez **`COMMANDES.md`** (plus pédagogique, avec exemples)
- **Vous voulez aller vite** → consultez **`AIDE-MEMOIRE.txt`** (compact, format cheatsheet)
- **Vous écrivez un article** → la section *Audit & citations scientifiques* du `COMMANDES.md`

## 🚀 Démarrage de Gabriel

```powershell
# Sans Isabelle (rapide, ~5 secondes)
.\start-agent.ps1

# Avec Isabelle/HOL (premier lancement long : ~30 minutes de téléchargement)
.\start-agent.ps1 -WithIsabelle
```

Une fois lancé, tapez `aide` dans Gabriel pour rappeler la liste des commandes.

## 📝 Maintenance

Si vous ajoutez de nouvelles commandes à Gabriel (`src/ui/cli.py`),
pensez à mettre à jour ces deux fichiers pour rester synchronisés avec
le code. Le `HELP_TEXT` dans `src/ui/cli.py` reste la source de vérité technique.

---

_Version : 2.2 — 15 février 2026 — 230/230 tests ✅_
