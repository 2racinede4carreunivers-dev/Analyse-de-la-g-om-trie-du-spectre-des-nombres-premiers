# Gabriel - 300 Templates (Isabelle + Texte + LaTeX)

## ✅ Fichiers créés

### Structure complète

```
theories/projects/
├── projet_uni_car_savard_01.thy
├── projet_uni_car_savard_02.thy
├── ...
├── projet_uni_car_savard_100.thy
│
├── txt/
│   ├── projet_uni_car_savard_01.txt
│   ├── projet_uni_car_savard_02.txt
│   ├── ...
│   └── projet_uni_car_savard_100.txt
│
└── tex/
    ├── projet_uni_car_savard_01.tex
    ├── projet_uni_car_savard_02.tex
    ├── ...
    └── projet_uni_car_savard_100.tex
```

**Total: 300 fichiers vierges**
- ✅ 100 fichiers `.thy` (Isabelle/HOL)
- ✅ 100 fichiers `.txt` (Texte brut)
- ✅ 100 fichiers `.tex` (LaTeX pour PDF)

---

## Usage des 3 types de fichiers

### Type 1: `.thy` (Isabelle/HOL)

**Pour:** Vérification formelle des théorèmes

**Structure:**
```isabelle
theory Savard_Project_001
  imports Main
begin

(* Définitions *)
(* TODO: ... *)

(* Lemmes préliminaires *)
(* TODO: ... *)

(* Théorème principal *)
(* TODO: ... *)

(* Preuves *)
(* TODO: ... *)

end
```

**Workflow Gabriel:**
```
1. Gabriel génère une théorie mathématique
2. Remplit le fichier .thy
3. Envoie à Isabelle CLI pour vérification
4. Récupère le résultat (valid/error)
5. Utilise le résultat pour sa réponse
```

---

### Type 2: `.txt` (Texte brut)

**Pour:** Documentation et explications textuelles

**Structure:**
```
Projet: projet_uni_car_savard_42
Univers au Carré - Méthode Spectrale Savard

Description: [À remplir]
Date création: [À remplir]
Statut: [VIERGE/EN COURS/TERMINÉ]

CONTENU
[À remplir]

NOTES
[À remplir]

RÉFÉRENCES
[À remplir]
```

**Workflow Gabriel:**
```
1. Gabriel écrit des explications textuelles
2. Remplit le fichier .txt avec la description
3. Peut être affiche directement sur www.universestaucarre.com
4. Archive pour la traçabilité
```

---

### Type 3: `.tex` (LaTeX)

**Pour:** Génération de PDF scientifiques

**Structure:**
```latex
\documentclass[12pt]{article}
\usepackage[utf-8]{inputenc}
\usepackage[french]{babel}
\usepackage{amsmath, amssymb}

\title{projet_uni_car_savard_42}
\author{Gabriel - Univers au Carré}
\date{\today}

\begin{document}
\maketitle

\section{Introduction}
% TODO: ...

\section{Définition et Notation}
% TODO: ...

\section{Théorème Principal}
\begin{equation}
% TODO: ...
\end{equation}

\section{Preuves}
% TODO: ...

\section{Résultats et Discussion}
% TODO: ...

\section{Conclusion}
% TODO: ...

\begin{thebibliography}{99}
% TODO: References
\end{thebibliography}

\end{document}
```

**Workflow Gabriel:**
```
1. Gabriel génère une preuve scientifique complète
2. Remplit le fichier .tex en LaTeX
3. Compile avec pdflatex → génère un PDF
4. Envoie le PDF à www.universestaucarre.com
5. Utilisateurs téléchargent le PDF
```

---

## Utilisation combinée

### Cas 1: Preuve mathématique complète

```
Gabriel a une question: "Vérifier que 101 est le 26ème nombre premier"

Étape 1: Créer la preuve Isabelle
  - Utiliser: /theories/projects/projet_uni_car_savard_26.thy
  - Remplir avec la théorie formelle
  - Vérifier avec Isabelle

Étape 2: Écrire l'explication
  - Utiliser: /theories/projects/txt/projet_uni_car_savard_26.txt
  - Expliquer la preuve en langage naturel

Étape 3: Générer un PDF scientifique
  - Utiliser: /theories/projects/tex/projet_uni_car_savard_26.tex
  - Compiler en PDF
  - Publier sur www.universestaucarre.com
```

**Résultat:**
- ✓ Preuve vérifiée formellement (Isabelle)
- ✓ Explication textuelle (TXT)
- ✓ Document scientifique (PDF/LaTeX)

---

## Dans le conteneur Docker

Les fichiers sont montés **automatiquement** en read-write:

```bash
# Accéder au conteneur Gabriel
docker exec -it llm-agent-multiloop-run bash

# Voir les fichiers
ls /theories/projects/
ls /theories/projects/txt/
ls /theories/projects/tex/

# Lire un fichier
cat /theories/projects/txt/projet_uni_car_savard_42.txt

# Modifier un fichier
echo "Nouveau contenu" > /theories/projects/txt/projet_uni_car_savard_42.txt
```

---

## Classe Gabriel pour gérer les 3 types

```python
from pathlib import Path

class GabrielMultiFormatManager:
    """Gère les projets multi-format (.thy, .txt, .tex)"""
    
    def __init__(self, projects_dir="/theories/projects"):
        self.projects_dir = Path(projects_dir)
        self.thy_dir = self.projects_dir
        self.txt_dir = self.projects_dir / "txt"
        self.tex_dir = self.projects_dir / "tex"
    
    def create_project(self, project_num, thy_content, txt_content, tex_content):
        """Crée un projet complet (Isabelle + Texte + LaTeX)"""
        
        # 1. Écrire la théorie Isabelle
        thy_file = self.thy_dir / f"projet_uni_car_savard_{project_num:02d}.thy"
        thy_file.write_text(thy_content)
        
        # 2. Écrire l'explication texte
        txt_file = self.txt_dir / f"projet_uni_car_savard_{project_num:02d}.txt"
        txt_file.write_text(txt_content)
        
        # 3. Écrire le document LaTeX
        tex_file = self.tex_dir / f"projet_uni_car_savard_{project_num:02d}.tex"
        tex_file.write_text(tex_content)
        
        return {
            "thy": str(thy_file),
            "txt": str(txt_file),
            "tex": str(tex_file)
        }
    
    def get_project_files(self, project_num):
        """Récupère tous les fichiers d'un projet"""
        return {
            "thy": self.thy_dir / f"projet_uni_car_savard_{project_num:02d}.thy",
            "txt": self.txt_dir / f"projet_uni_car_savard_{project_num:02d}.txt",
            "tex": self.tex_dir / f"projet_uni_car_savard_{project_num:02d}.tex",
        }
    
    def compile_latex_to_pdf(self, project_num):
        """Compile le fichier .tex en PDF"""
        import subprocess
        
        tex_file = self.tex_dir / f"projet_uni_car_savard_{project_num:02d}.tex"
        pdf_file = self.tex_dir / f"projet_uni_car_savard_{project_num:02d}.pdf"
        
        # pdflatex ou xelatex
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", str(tex_file)],
            cwd=str(self.tex_dir),
            capture_output=True
        )
        
        return {
            "success": result.returncode == 0,
            "pdf_file": str(pdf_file) if pdf_file.exists() else None
        }
```

---

## Montage Docker (déjà configuré)

Dans `docker-compose.yml`:

```yaml
llm-agent-multiloop:
  volumes:
    - ./theories:/theories  # Inclut tout: .thy, txt/, tex/

isabelle:
  volumes:
    - ./theories:/theories  # Accès complet
```

**Résultat:** Gabriel peut accéder à tous les fichiers sans rebuild image! ✓

---

## Commandes utiles

```bash
# Compter les fichiers de chaque type
ls /theories/projects/*.thy | wc -l       # 100
ls /theories/projects/txt/*.txt | wc -l   # 100
ls /theories/projects/tex/*.tex | wc -l   # 100

# Voir un projet complet
cat /theories/projects/projet_uni_car_savard_42.thy
cat /theories/projects/txt/projet_uni_car_savard_42.txt
cat /theories/projects/tex/projet_uni_car_savard_42.tex

# Compiler un PDF
cd /theories/projects/tex
pdflatex -interaction=nonstopmode projet_uni_car_savard_42.tex

# Voir les PDFs générés
ls /theories/projects/tex/*.pdf
```

---

## Avantages

| Avantage | Détail |
|----------|--------|
| ✅ 3 formats complémentaires | Isabelle (vérification) + Texte (explication) + LaTeX (PDF) |
| ✅ 300 fichiers au total | 3 × 100 pour scalabilité maximale |
| ✅ Pas de rebuild image | Tous les fichiers montés en read-write |
| ✅ Réutilisable | Chaque format peut être utilisé pour différents cas |
| ✅ Traçabilité complète | Chaque projet a tous les 3 formats |
| ✅ Génération PDF | LaTeX permet de créer des documents PDF professionnels |
| ✅ Workflow complet | Question → Théorie → Explication → Document |

---

## Workflow complet: Gabriel répond à www.universestaucarre.com

```
1. Utilisateur pose une question sur www.universestaucarre.com
   ↓
2. Gabriel traite la question
   ↓
3. Gabriel crée un projet complet (projet #42):
   - projet_uni_car_savard_42.thy (preuve Isabelle)
   - txt/projet_uni_car_savard_42.txt (explication)
   - tex/projet_uni_car_savard_42.tex (document LaTeX)
   ↓
4. Vérification:
   - Isabelle CLI vérifie la théorie
   - Validation réussie → Peut compiler le PDF
   ↓
5. Génération PDF:
   - pdflatex compile le .tex → PDF
   - PDF stocké: tex/projet_uni_car_savard_42.pdf
   ↓
6. Réponse à l'utilisateur:
   - Affiche l'explication (.txt)
   - Propose le téléchargement du PDF
   - Montre le statut de vérification Isabelle
```

---

## Structure finale complète

```
theories/
├── projects/
│   ├── projet_uni_car_savard_01.thy ← Isabelle
│   ├── projet_uni_car_savard_02.thy
│   ├── ...
│   ├── projet_uni_car_savard_100.thy
│   │
│   ├── txt/
│   │   ├── projet_uni_car_savard_01.txt ← Texte brut
│   │   ├── projet_uni_car_savard_02.txt
│   │   ├── ...
│   │   └── projet_uni_car_savard_100.txt
│   │
│   └── tex/
│       ├── projet_uni_car_savard_01.tex ← LaTeX
│       ├── projet_uni_car_savard_01.pdf ← Généré
│       ├── projet_uni_car_savard_02.tex
│       ├── projet_uni_car_savard_02.pdf
│       ├── ...
│       ├── projet_uni_car_savard_100.tex
│       └── projet_uni_car_savard_100.pdf
│
├── generated/           ← Projets remplis
├── archives/           ← Projets terminés (optionnel)
└── ...
```

---

## Prochaines étapes

1. ✅ **100 .thy créés** (Isabelle vérification)
2. ✅ **100 .txt créés** (Explication texte)
3. ✅ **100 .tex créés** (Document LaTeX)
4. ⏳ **Intégrer GabrielMultiFormatManager** dans Gabriel
5. ⏳ **Compiler les PDFs** automatiquement
6. ⏳ **Interfacer avec www.universestaucarre.com** pour PDF download

---

## Résumé

**Tu as maintenant 300 fichiers vierges montés dans Docker:**
- Pour la vérification formelle (Isabelle)
- Pour la documentation (Texte)
- Pour les publications scientifiques (LaTeX/PDF)

**SANS rebuild image, Gabriel peut les utiliser immédiatement!** 🚀

---

**Version:** 4.0 + Multi-Format Templates  
**Status:** ✅ Ready to use  
**Fichiers:** 100 .thy + 100 .txt + 100 .tex = 300 total
