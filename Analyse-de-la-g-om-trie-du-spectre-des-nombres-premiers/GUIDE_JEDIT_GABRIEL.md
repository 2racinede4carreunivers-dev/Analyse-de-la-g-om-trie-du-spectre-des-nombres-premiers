# Guide: Gabriel + Isabelle Jed it Integration

## Résumé rapide

Tu veux que Gabriel **génère du code Isabelle** et que **Jed it le vérifie**, correct?

```
Gabriel (question)
    ↓
Gabriel génère: theorem_proof.thy
    ↓
Écrit dans: /theories/generated_*.thy
    ↓
Jed it ouvre le fichier (interactif)
OU
Isabelle CLI vérifie le fichier (batch)
    ↓
Résultat retourné à Gabriel
    ↓
Gabriel affiche: "✓ Vérifié par Isabelle"
```

---

## Option A: Jed it GUI (Interactive)

### Sur Windows avec Docker Desktop:

Tu veux faire:
```bash
1. docker-compose up -d
2. docker exec -it llm-agent-multiloop-run bash
3. isabelle jedit
```

**Le problème:** Jed it est une **GUI X11** qui ne peut pas s'afficher sur Windows directement.

### Solution: VcXsrv (X11 server pour Windows)

#### Étape 1: Installer VcXsrv

1. Télécharger: https://sourceforge.net/projects/vcxsrv/
2. Installer (accepter les defaults)

#### Étape 2: Configurer le docker-compose.yml

Modifier le service `isabelle`:

```yaml
isabelle:
  image: makarius/isabelle:latest
  container_name: isabelle
  restart: unless-stopped
  profiles: ["isabelle"]
  
  # v4.0 avec support Jed it GUI
  environment:
    - DISPLAY=host.docker.internal:0
    - QT_QPA_PLATFORM=xcb
    # Alternativement (si xcb ne marche pas):
    # - QT_QPA_PLATFORM=offscreen
  
  volumes:
    - ./theories:/theories
    - isabelle-heaps:/home/isabelle/.isabelle/heaps
    # IMPORTANT: Mount X11 socket
    - /tmp/.X11-unix:/tmp/.X11-unix:rw
  
  networks:
    - agent-network
  
  entrypoint: ["/bin/bash"]
  command: ["-c", "tail -f /dev/null"]  # Juste rester actif
```

#### Étape 3: Lancer Jed it

```bash
# 1. Lancer VcXsrv sur Windows (avant docker-compose)
# VcXsrv → Lancer X server (default settings)

# 2. Lancer les services
docker-compose --profile isabelle up -d

# 3. Accéder au conteneur Isabelle
docker exec -it isabelle bash

# 4. Lancer Jed it
isabelle jedit /theories/example.thy
```

Jed it devrait s'afficher sur ton écran Windows!

---

## Option B: Jed it CLI Batch (RECOMMANDÉ pour Windows)

C'est plus pratique et ne nécessite pas de configuration X11:

```bash
# 1. Lancer les services avec profil Isabelle
docker-compose --profile isabelle up -d

# 2. Isabelle CLI traite les fichiers .thy automatiquement
# Aucune interaction manuelle nécessaire!

# 3. Les résultats sont disponibles dans /theories/generated/
```

**Comment ça fonctionne:**

Le script `scripts/isabelle-integration.sh`:
1. Surveille `/theories` pour les fichiers `.thy`
2. Les traite avec `isabelle process -o quick`
3. Sauvegarde les résultats
4. Envoie les résultats à Gabriel via HTTP API

---

## Gabriel AGIT dans Jed it

### Workflow complet:

```python
# 1. Gabriel génère une théorie
thy_file = bridge.generate_isabelle_theory(
    question="Quel est le 26eme nombre premier?",
    answer="Le 26ème nombre premier est 101."
)
# Crée: /theories/generated_1234567890.thy

# 2. Gabriel envoie à Isabelle
result = await bridge.verify_with_isabelle(thy_file, mode="cli")
# Retourne: {"valid": True, "output": "...", "errors": ""}

# 3. Gabriel utilise le résultat
if result["valid"]:
    print("✓ Vérifié par Isabelle!")
else:
    print("✗ Erreur de vérification:")
    print(result["errors"])
```

### Code pour Gabriel:

```python
from src.adapters.gabriel_isabelle_bridge import GabrielIsabelleBridge

class GabrielWithIsabelle:
    def __init__(self):
        self.bridge = GabrielIsabelleBridge()
    
    async def answer_with_verification(self, question: str):
        """Gabriel répond avec vérification Isabelle"""
        
        # 1. Gabriel répond normalement
        answer = self.multiloop_process(question)
        
        # 2. Si c'est une question mathématique → vérifier avec Isabelle
        if self._is_mathematical(question):
            result = await self.bridge.full_workflow(
                question=question,
                gabriel_answer=answer,
                use_jedit=False  # Mode CLI batch
            )
            
            if result["isabelle_valid"]:
                return f"{answer}\n✓ Vérifié par Isabelle (fichier: {result['theory_file']})"
            else:
                return f"{answer}\n⚠ Vérification échouée:\n{result['verification']['errors']}"
        
        return answer
```

---

## Commandes complètes

### Étape 1: Setup initial

```bash
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local

# Option A: Avec Jed it GUI (VcXsrv requis)
docker-compose --profile isabelle up -d

# Option B: Avec Isabelle CLI batch (recommandé)
docker-compose --profile isabelle up -d
```

### Étape 2: Si tu veux utiliser Jed it GUI interactif

```bash
# Vérifier que les conteneurs tournent
docker ps

# Accéder au conteneur Isabelle
docker exec -it isabelle bash

# Vérifier la connexion X11
echo $DISPLAY

# Lancer Jed it
isabelle jedit /theories/example.thy
```

### Étape 3: Gabriel génère et vérifie

```bash
# Accéder au conteneur Gabriel
docker exec -it llm-agent-multiloop-run bash

# Depuis Python:
python3 << 'EOF'
import asyncio
from src.adapters.gabriel_isabelle_bridge import GabrielIsabelleBridge

async def test():
    bridge = GabrielIsabelleBridge()
    result = await bridge.full_workflow(
        "Quel est le 26eme nombre premier?",
        "Le 26ème nombre premier est 101."
    )
    print(result)

asyncio.run(test())
EOF
```

---

## Fichiers créés/modifiés

| Fichier | Description |
|---------|-------------|
| `src/adapters/gabriel_isabelle_bridge.py` | **Bridge Gabriel ↔ Isabelle** |
| `docker-compose.yml` | Modifié pour X11 (Jed it GUI) |
| `scripts/isabelle-integration.sh` | Batch mode (surveille /theories) |

---

## FAQ

### Q: Je peux vraiment utiliser Jed it sur Windows?

**R:** Oui, mais il faut VcXsrv. Sinon, utilise le mode CLI batch qui est plus simple et fonctionne partout.

### Q: Comment faire agir Gabriel DANS Jed it?

**R:** Gabriel génère un fichier `.thy` → Jed it l'ouvre → L'utilisateur le modifie → Gabriel récupère le résultat.

Alternativement (recommandé): Gabriel génère → Isabelle CLI vérifie → Gabriel utilise le résultat.

### Q: Mes commandes docker exec -it ne fonctionnent pas?

**R:** Utilise:
```bash
# À la place de:
# docker exec -it gabriel agent bash

# Utilise:
docker exec -it llm-agent-multiloop-run bash
```

(Le nom du conteneur est `llm-agent-multiloop-run`, pas `gabriel agent`)

### Q: Comment j'intègre ça avec www.universestaucarre.com?

**R:** Gabriel génère → Vérifie avec Isabelle → Retourne le résultat via HTTP API (port 8000) → www.universestaucarre.com l'affiche.

```javascript
// Sur www.universestaucarre.com
const result = await fetch("http://localhost:8000/query", {
  method: "POST",
  body: JSON.stringify({
    question: "Quel est le 26eme nombre premier?",
    require_proof: true  // Gabriel utilisera Isabelle
  })
});
```

---

## Diagramme du workflow complet

```
┌──────────────────────────────────────────────────────────┐
│ www.universestaucarre.com (utilisateur)                  │
│ "Quel est le 26eme nombre premier?"                      │
└──────────────┬───────────────────────────────────────────┘
               │ HTTP POST /query
               ↓
┌──────────────────────────────────────────────────────────┐
│ GABRIEL (Docker)                                         │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ 1. Traiter la question (multiloop)                  │ │
│ │ 2. Générer réponse: "97"                            │ │
│ │ 3. Vérifier avec Isabelle?                          │ │
│ │    OUI → Bridge→Isabelle                            │ │
│ └──────────────────────────────────────────────────────┘ │
└──────────────┬───────────────────────────────────────────┘
               │
               ↓
┌──────────────────────────────────────────────────────────┐
│ ISABELLE (Docker)                                        │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ Mode 1 (CLI batch):                                 │ │
│ │  isabelle process -o quick /theories/generated.thy  │ │
│ │  → Retour: {valid: true, output: "..."}            │ │
│ │                                                      │ │
│ │ Mode 2 (Jed it GUI - Windows + VcXsrv):            │ │
│ │  isabelle jedit /theories/generated.thy             │ │
│ │  → Utilisateur modifie / vérifie manuellement      │ │
│ └──────────────────────────────────────────────────────┘ │
└──────────────┬───────────────────────────────────────────┘
               │
               ↓
┌──────────────────────────────────────────────────────────┐
│ GABRIEL (retour)                                         │
│ Réponse finale: "97 ✓ Vérifié par Isabelle"            │
└──────────────┬───────────────────────────────────────────┘
               │ HTTP Response
               ↓
┌──────────────────────────────────────────────────────────┐
│ www.universestaucarre.com                                │
│ Affiche: "Le 26ème nombre premier est 97 ✓"            │
└──────────────────────────────────────────────────────────┘
```

---

## Prochaines étapes

1. **Tester le mode CLI batch** (recommandé)
   ```bash
   docker-compose --profile isabelle up -d
   docker logs isabelle
   ```

2. **Si tu veux Jed it GUI:**
   - Installer VcXsrv
   - Configurer DISPLAY dans docker-compose.yml
   - `docker exec -it isabelle bash; isabelle jedit /theories/example.thy`

3. **Intégrer avec www.universestaucarre.com:**
   - Gabriel génère → Vérifie avec Isabelle → HTTP Response
   - Voir `INTEGRATION_UNIVERSESTAUCARRE.md`

---

**Version:** 4.0 (2025-01-15)  
**Status:** Prêt pour test  
**Auteur:** Gordon
