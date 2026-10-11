# Guide: Connecter www.universestaucarre.com a Gabriel Local

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ www.universestaucarre.com (4 IAs: GPT4, Claude, Gemini, Gabriel)│
│ (Serveur: emergent.sh - externe)                                │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   │ HTTP POST /sync/universestaucarre
                   │ (localhost:8000 ou domain.com:8000)
                   ↓
┌─────────────────────────────────────────────────────────────────┐
│ GABRIEL LOCAL (Docker)                                          │
│ ┌──────────────────────────────────────────────────────────────┤
│ │ Port 8000: HTTP API                                          │
│ │ - POST /query → Repondre a une question                     │
│ │ - POST /sync/universestaucarre → Synchro avec le site web  │
│ │ - POST /isabelle/verify → Resultats Isabelle CLI            │
│ │ - GET /health → Verifier que Gabriel est en ligne           │
│ └──────────────────────────────────────────────────────────────┤
│                                                                  │
│ Services:                                                        │
│  - llm-agent-multiloop (Gabriel - Python)                      │
│  - isabelle (HOL - mode CLI batch)                             │
│  - ollama (LLM local - Llama 3.2)                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Etape 1: Lancer Gabriel avec Isabelle CLI

```bash
# Depuis Windows (PowerShell)
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local

# Mode CLI Isabelle (sans Jed it GUI)
docker-compose --profile isabelle up -d

# Ou sans Isabelle si pas besoin
docker-compose up -d
```

Verifier que Gabriel ecoute sur le port 8000:

```bash
# Test 1: Depuis le host (Windows)
curl http://localhost:8000/health

# Test 2: Depuis le conteneur Gabriel
docker exec llm-agent-multiloop-run curl http://0.0.0.0:8000/health
```

Expected response:
```json
{
  "status": "online",
  "service": "Gabriel v4.0",
  "pipeline": "active",
  "timestamp": "2025-01-15T14:30:00.000000"
}
```

---

## Etape 2: Configurer www.universestaucarre.com pour envoyer requetes a Gabriel

### Option A: Connection locale (sur le meme reseau/machine)

```javascript
// Code sur www.universestaucarre.com (JavaScript/Node.js)
const GABRIEL_LOCAL_URL = "http://localhost:8000";

async function queryGabriel(question) {
  try {
    const response = await fetch(`${GABRIEL_LOCAL_URL}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: question,
        source: "universestaucarre"
      })
    });
    
    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Gabriel local indisponible:", error);
    return null;
  }
}

// Exemple:
const answer = await queryGabriel("Qu'est-ce que l'univers au carre?");
console.log(answer.answer);
```

### Option B: Connection distante (via domaine ou IP)

Si www.universestaucarre.com est **sur une machine differente**:

1. Obtenir l'IP locale de Gabriel:
```bash
# Sur Windows
ipconfig
# Chercher l'IPv4 Address (ex: 192.168.1.100)

# Ou depuis Docker:
docker inspect llm-agent-multiloop-run | grep IPAddress
```

2. Autoriser les connexions externes dans docker-compose.yml:
```yaml
llm-agent-multiloop:
  ports:
    - "0.0.0.0:8000:8000"  # Expose sur toutes les interfaces
```

3. Dans www.universestaucarre.com, utiliser l'IP ou domaine:
```javascript
const GABRIEL_LOCAL_URL = "http://192.168.1.100:8000";
// ou si tu as un nom de domaine:
// const GABRIEL_LOCAL_URL = "http://gabriel-local.home:8000";
```

---

## Etape 3: Endpoint de Synchronisation

### POST /sync/universestaucarre

Envoyer les resultats de toutes les 4 IAs a Gabriel pour comparaison:

```javascript
async function syncWithGabriels(question, results) {
  const response = await fetch("http://localhost:8000/sync/universestaucarre", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      session_id: "uuid-" + Date.now(),
      question: question,
      results: {
        gpt4: results.gpt4,
        claude: results.claude,
        gemini: results.gemini,
        gabriel_web: results.gabriel  // Version web (emergent.sh)
      }
    })
  });
  
  const synced = await response.json();
  return synced;
}

// Exemple complet:
async function compareAllIAs(question) {
  // 1. Appeler les 4 IAs (GPT4, Claude, Gemini, Gabriel Web)
  const results = {
    gpt4: await queryGPT4(question),
    claude: await queryClaude(question),
    gemini: await queryGemini(question),
    gabriel: "..." // Resultat depuis emergent.sh
  };
  
  // 2. Synchroniser avec Gabriel LOCAL
  const localComparison = await syncWithGabriels(question, results);
  
  // 3. Afficher la comparaison
  console.log("Gabriel Local vs Web:", localComparison);
  
  return localComparison;
}
```

---

## Etape 4: Integration Isabelle CLI

### Workflow: www.universestaucarre.com → Gabriel → Isabelle

```
1. Utilisateur pose une question sur www.universestaucarre.com
   ↓
2. POST http://localhost:8000/query
   ↓
3. Gabriel traite la question (spectral, multiloop, etc.)
   ↓
4. Si besoin de verification HOL → POST /isabelle/verify
   ↓
5. Isabelle (CLI mode) traite le fichier .thy
   ↓
6. Resultat retourne a Gabriel
   ↓
7. Reponse finale envoyee a www.universestaucarre.com
```

### Exemple d'une question necessitant Isabelle:

```json
POST http://localhost:8000/query
{
  "question": "Verifiez formellement que le 25eme nombre premier est 97",
  "source": "universestaucarre",
  "require_proof": true
}
```

Gabriel repondra:
```json
{
  "answer": "97 est bien le 25eme nombre premier. Verification HOL en cours...",
  "confidence": 0.95,
  "hol_script": "theory Verify_P25 imports Main begin...",
  "isabelle_status": "verified",
  "timestamp": "2025-01-15T14:35:00.000000"
}
```

---

## Etape 5: Monitoring et Debug

### Verifier les logs:

```bash
# Logs Gabriel
docker logs llm-agent-multiloop-run

# Logs Isabelle
docker logs isabelle

# Logs Ollama
docker logs ollama
```

### Verifier les fichiers de synchro:

```bash
# Depuis Windows
dir "C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local\data\universestaucarre-sync"

# Depuis le conteneur
docker exec llm-agent-multiloop-run ls -la /home/agent/app/data/universestaucarre-sync/
```

### Tester manuellement:

```bash
# Test 1: Simple query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Quel est le 10eme nombre premier?", "source": "test"}'

# Test 2: Sync
curl -X POST http://localhost:8000/sync/universestaucarre \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "test-123",
    "question": "La physique quantique existe-t-elle?",
    "results": {"gpt4": "Oui", "claude": "Oui", "gemini": "Oui", "gabriel_web": "Oui"}
  }'

# Test 3: Health check
curl http://localhost:8000/health
```

---

## Etape 6: Configuration pour Production

### Domaine personnalisé:

Si tu veux que www.universestaucarre.com accede a Gabriel via un nom de domaine:

1. **Option DNS local:**
   ```
   gabriel-local.home  →  192.168.1.100:8000
   ```

2. **Option Reverse Proxy (Nginx):**
   ```nginx
   upstream gabriel {
       server llm-agent-multiloop-run:8000;
   }
   
   server {
       listen 8000;
       server_name gabriel-local.home;
       
       location / {
           proxy_pass http://gabriel;
       }
   }
   ```

3. **Option SSL/TLS (pour HTTPS):**
   ```bash
   # Generer certificate autosigne
   openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
   ```

---

## Questions/Issues Courants

### Q: www.universestaucarre.com ne peut pas atteindre Gabriel sur localhost:8000

**A:** C'est normal si le site est sur une autre machine. Utilise:
```
http://192.168.1.100:8000  (l'IP locale de Gabriel)
```

### Q: Isabelle CLI ne se lance pas

**A:** Verifier les logs:
```bash
docker logs isabelle
```

Si erreur "inotify-tools not found", c'est OK - le script utilisera le polling.

### Q: Les resultats d'Isabelle ne sont pas envoyes a Gabriel

**A:** Verifier que Gabriel ecoute sur le port 8000:
```bash
docker exec llm-agent-multiloop-run curl http://0.0.0.0:8000/health
```

### Q: Comment arreter Gabriel proprement?

**A:**
```bash
docker-compose down
```

---

## Fichiers cles pour cette integration

- `docker-compose.yml` - Configuration des services (v4.0)
- `scripts/isabelle-integration.sh` - Script CLI Isabelle
- `src/api/gabriel_http_api.py` - HTTP API endpoints
- `main_cli.py` - Entry point qui lance l'API Flask

---

## Prochaines etapes

1. **Integration WebSocket** - Pour streaming temps reel
2. **Cache Redis** - Pour eviter les recalculs
3. **Rate Limiting** - Pour proteger Gabriel de surcharge
4. **Authentification** - Pour securiser www.universestaucarre.com

---

**Version:** 4.0 (2025-01-15)
**Auteur:** Gordon (Docker Assistant)
**Status:** Documentation - Pret pour test
