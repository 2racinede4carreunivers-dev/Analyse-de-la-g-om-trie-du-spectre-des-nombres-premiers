# Gabriel - Utilisation des Templates Isabelle (.thy)

## ✅ 100 fichiers vierges créés!

Les 100 fichiers templates Isabelle ont été générés dans:

```
C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local\theories\projects\
```

Nomenclature:
- `projet_uni_car_savard_01.thy`
- `projet_uni_car_savard_02.thy`
- ...
- `projet_uni_car_savard_100.thy`

---

## Comment Gabriel les utilise

### Workflow: Gabriel → Réutilise un template → Remplit le contenu

```python
# 1. Gabriel veut créer un nouveau projet
question = "Vérifier que 101 est premier"

# 2. Gabriel cherche un template vierge disponible
template_number = 42  # Projet 42 est libre
template_file = f"/theories/projects/projet_uni_car_savard_{template_number:02d}.thy"

# 3. Gabriel lit le template vierge
with open(template_file) as f:
    template_content = f.read()

# 4. Gabriel remplit le template avec sa théorie
new_content = template_content.replace(
    "TODO: Ajouter le théorème principal",
    f"theorem p_is_prime: \"prime 101\" by ..."
)

# 5. Gabriel écrit dans le même fichier (ou crée /generated/)
output_file = f"/theories/generated/projet_uni_car_savard_{template_number:02d}_execution.thy"
with open(output_file, 'w') as f:
    f.write(new_content)

# 6. Isabelle vérifie le fichier
result = subprocess.run(["isabelle", "process", output_file])
```

---

## Structure du template

Chaque fichier contient:

```isabelle
(* ============================================================
 * Projet: projet_uni_car_savard_42
 * Univers au Carré - Méthode Spectrale Savard
 * 
 * Description: [À remplir par Gabriel/utilisateur]
 * Date création: [À remplir]
 * Statut: [VIERGE/EN COURS/TERMINÉ]
 * ============================================================ *)

theory Savard_Project_042
  imports Main
begin

(* ============================================================
 * SECTION 1 : Définitions
 * ============================================================ *)
(* TODO: Ajouter les définitions *)

(* ============================================================
 * SECTION 2 : Lemmes préliminaires
 * ============================================================ *)
(* TODO: Ajouter les lemmes *)

(* ============================================================
 * SECTION 3 : Théorème principal
 * ============================================================ *)
(* TODO: Ajouter le théorème principal *)

(* ============================================================
 * SECTION 4 : Preuves
 * ============================================================ *)
(* TODO: Ajouter les preuves *)

end
```

---

## Dans le conteneur Docker

Les fichiers sont montés **automatiquement** en read-write:

```bash
# Depuis Gabriel container
docker exec -it llm-agent-multiloop-run bash

# Les fichiers sont accessibles:
ls /theories/projects/
# projet_uni_car_savard_01.thy
# projet_uni_car_savard_02.thy
# ...
# projet_uni_car_savard_100.thy

# Gabriel peut les lire/modifier
cat /theories/projects/projet_uni_car_savard_42.thy
```

---

## Avantages de cette approche

✅ **Pas de rebuild image**: Tu ajoutes des projets sans `docker build`

✅ **Réutilisable**: Chaque projet peut être utilisé plusieurs fois

✅ **Structure uniforme**: Tous les projets suivent le même format

✅ **Traçabilité**: Chaque projet a un numéro et une date

✅ **Évolutif**: Tu peux ajouter plus de templates à l'avenir

✅ **Persistant**: Les modifications sont sauvegardées sur le host

---

## Cas d'utilisation

### Cas 1: Gabriel crée un nouveau projet

```python
# Gabriel a une nouvelle question mathématique
# Il utilise le template 15
template = "/theories/projects/projet_uni_car_savard_15.thy"

# Gabriel le remplit avec sa théorie
# Envoie au conteneur Isabelle
# Récupère les résultats

# Le template 15 a maintenant du contenu, passe au template 16 pour le prochain projet
```

### Cas 2: Tu veux modifier manuellement un projet

```bash
# Ouvre un fichier dans Jed it ou un éditeur
code C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local\theories\projects\projet_uni_car_savard_05.thy

# Modifie le contenu
# Sauvegarde
# Gabriel le détecte et peut le vérifier avec Isabelle
```

### Cas 3: Archivage des projets

```bash
# Une fois terminé, le projet peut être archivé
mv /theories/projects/projet_uni_car_savard_15.thy /theories/archives/completed_15.thy

# Un nouveau template vierge peut être créé à la place
```

---

## Configuration Gabriel pour utiliser les templates

Ajoute cette fonction à `src/adapters/gabriel_isabelle_bridge.py`:

```python
import os
from pathlib import Path

class GabrielProjectManager:
    """Gère les projets Isabelle vierges et remplis"""
    
    def __init__(self, projects_dir="/theories/projects"):
        self.projects_dir = Path(projects_dir)
        self.generated_dir = self.projects_dir.parent / "generated"
        self.generated_dir.mkdir(exist_ok=True)
    
    def find_next_available_project(self):
        """Trouve le prochain projet vierge disponible"""
        for i in range(1, 101):
            project_name = f"projet_uni_car_savard_{i:02d}"
            project_file = self.projects_dir / f"{project_name}.thy"
            
            if project_file.exists():
                # Vérifier si vierge (contient TODO)
                content = project_file.read_text()
                if "TODO:" in content:
                    return i, project_file
        
        return None, None
    
    def create_project_from_template(self, template_num, theory_content):
        """Crée un projet rempli à partir d'un template vierge"""
        template_file = self.projects_dir / f"projet_uni_car_savard_{template_num:02d}.thy"
        output_file = self.generated_dir / f"execution_projet_{template_num:02d}.thy"
        
        template_content = template_file.read_text()
        
        # Remplacer les TODO
        filled_content = template_content.replace(
            "TODO: Ajouter le théorème principal",
            theory_content
        )
        
        output_file.write_text(filled_content)
        return str(output_file)
```

---

## Commandes pour gérer les templates

```bash
# Voir tous les templates
ls -la /theories/projects/ | wc -l

# Voir les templates vierges (avec TODO)
grep -l "TODO:" /theories/projects/*.thy | wc -l

# Voir un template spécifique
cat /theories/projects/projet_uni_car_savard_42.thy

# Compter les projets utilisés
find /theories/generated/ -name "*execution_projet_*.thy" | wc -l
```

---

## Structure des dossiers

```
theories/
├── projects/                    ← Templates VIERGES (100 fichiers)
│   ├── projet_uni_car_savard_01.thy
│   ├── projet_uni_car_savard_02.thy
│   ├── ...
│   └── projet_uni_car_savard_100.thy
│
├── generated/                   ← Projets REMPLIS par Gabriel
│   ├── execution_projet_01.thy  ← Gabriel a utilisé template 01
│   ├── execution_projet_02.thy
│   └── ...
│
└── archives/                    ← Projets TERMINÉS (optionnel)
    ├── completed_01.thy
    └── ...
```

---

## Montage Docker (déjà configuré)

Dans `docker-compose.yml`, les volumes sont déjà configurés:

```yaml
llm-agent-multiloop:
  volumes:
    - ./theories:/theories              # Tout le dossier theories/
    - ./theories:/home/agent/app/theories:ro  # Read-only pour app
```

Isabelle:
```yaml
isabelle:
  volumes:
    - ./theories:/theories              # Accès complet
```

Les deux conteneurs voient les mêmes fichiers! ✓

---

## Prochaines étapes

1. ✅ **100 templates créés** (fait!)
2. ✅ **Montés dans Docker** (déjà configuré)
3. ⏳ **Gabriel les utilise** (à implémenter dans la logique Gabriel)
4. ⏳ **Interface pour les visualiser** (futur)

---

## Test: Vérifier que les fichiers sont accessibles

```bash
# Dans Gabriel container
docker exec -it llm-agent-multiloop-run bash

# Vérifier les templates
ls /theories/projects/ | head

# Compter
ls /theories/projects/ | wc -l

# Lire un template
cat /theories/projects/projet_uni_car_savard_01.thy
```

---

**Résumé:** Tu as maintenant 100 fichiers `.thy` vierges, montés dans Docker, que Gabriel peut remplir au fur et à mesure sans refaire l'image! 🎯

**Version:** 4.0 + Projets Templates  
**Status:** ✅ Ready to use  
**Fichiers:** 100 x projet_uni_car_savard_*.thy
