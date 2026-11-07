╔════════════════════════════════════════════════════════════════════════════╗
║      QUICK START - SCHÉMAS, FIGURES ET VISION GABRIEL                      ║
║                                                                            ║
║  Activation en 2 étapes simples                                           ║
╚════════════════════════════════════════════════════════════════════════════╝

## FICHIERS CRÉÉS (Déjà en place ✓)

✓ src/core/generateur_schemas_avances.py    (17.9 KB)
✓ src/core/vision_gabriel.py                (10.1 KB)

## ÉTAPE 1: Tester les schémas

```bash
cd C:\agent-multiloop-Gabriel-local-final\src\core

# Lancer démo schémas
python generateur_schemas_avances.py

# Résultat: Voir 6 types de schémas ASCII
```

## ÉTAPE 2: Tester la vision

```bash
# Lancer démo vision
python vision_gabriel.py

# Résultat: Voir commandes disponibles
```

## ÉTAPE 3: Intégrer dans Gabriel

Modifier: `src/core/integrateur_memoire.py`

```python
# Ajouter imports
from src.core.generateur_schemas_avances import GenerateurSchemasAvances
from src.core.vision_gabriel import TerminalVisionGabriel

# Dans __init__:
self.schemas = GenerateurSchemasAvances()
self.vision = TerminalVisionGabriel()

# Dans traiter_requete:
async def traiter_requete(self, question: str):
    # Vision: vérifier commandes !image
    analyse_image = self.vision.processer_commande_terminal(question)
    if analyse_image:
        question = analyse_image + "\n" + question
    
    # LLM réponse
    response = await self.llm_router.route_request(question)
    
    # Enrichir avec géométrie et schémas
    response_enrichie = enrichir_reponse_gabriel(response)
    
    return response_enrichie
```

## ÉTAPE 4: Rebuild et Relancer

```bash
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local

docker-compose build --no-cache
docker-compose up -d
```

## UTILISATION

### Générer schémas:
```
Requête: "Montre-moi l'organigramme du processus"
Gabriel: [Organigramme ASCII généré]
```

### Analyser images:
```
Terminal: !image C:\mon_image.png
Requête: "Peux-tu analyser cette image?"
Gabriel: [Analyse + schémas générés]
```

## VOILÀ! ✅

Gabriel génère maintenant:
✓ Schémas professionnels (diagrammes, arbres, circuits)
✓ Peut lire tes images
✓ Combine tout pour réponses visuelles complètes
