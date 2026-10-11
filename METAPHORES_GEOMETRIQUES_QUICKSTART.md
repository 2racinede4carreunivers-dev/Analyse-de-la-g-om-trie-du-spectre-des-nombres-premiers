╔════════════════════════════════════════════════════════════════════════════╗
║           QUICK START - MÉTAPHORES GÉOMÉTRIQUES GABRIEL                   ║
║                                                                            ║
║  3 étapes pour activer les représentations spatiales automatiques         ║
╚════════════════════════════════════════════════════════════════════════════╝

## ÉTAPE 1: Verifier que les fichiers sont en place

```bash
Vérifier:
✓ src/core/metaphore_geometrique.py               (18.3 KB)
✓ src/core/gabriel_geometric_wrapper.py           (7.4 KB)
```

## ÉTAPE 2: Modifier integrateur_memoire.py

Ouvre: `src/core/integrateur_memoire.py`

Cherche la méthode `traiter_requete()` (environ ligne 150-200)

**AVANT:**
```python
async def traiter_requete(self, question: str):
    # ...
    response = await self.llm_router.route_request(question)
    return response  # ← Retour direct
```

**APRÈS:**
```python
async def traiter_requete(self, question: str):
    # ...
    from src.core.gabriel_geometric_wrapper import enrichir_reponse_gabriel
    
    response = await self.llm_router.route_request(question)
    
    # ✓ AJOUTER CETTE LIGNE:
    response_enrichie = enrichir_reponse_gabriel(response)
    
    return response_enrichie  # ← Retour enrichi
```

## ÉTAPE 3: Rebuild et Redémarrer

```bash
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local

# Rebuild (pour inclure nouveaux fichiers)
docker-compose build --no-cache

# Démarrer
docker-compose up -d
```

## TEST

Requête:
```
"Montre moi graphiquement la convergence du ratio vers 1/2 
pour k=1 à k=10"
```

Résultat attendu:
```
[Réponse textuelle normale]

╔═══════════════════════════════════════════════════════════╗
║  STRUCTURE GÉOMÉTRIQUE SPATIALE - Convergence Analysée
╚═══════════════════════════════════════════════════════════╝

[Graphique ASCII]
[Coordonnées 3D]
[Matrice de points]
[Instructions de modélisation]
```

═══════════════════════════════════════════════════════════════════════════

## VOILÀ! 

Gabriel génère maintenant automatiquement des représentations spatiales 
pour chaque réponse! 🎨📐

Tu peux maintenant:
- Copier les points 3D dans FreeCAD
- Utiliser les instructions dans Blender
- Exporter en STL pour impression 3D
- Visualiser la géométrie spectrale directement!
