# Gabriel v4.0 - Liste COMPLÈTE des Commandes (ÉTENDUE)

## SECTION 1: DÉMARRAGE ET ARRÊT

### Démarrer Gabriel (mode standard)
```powershell
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local
docker-compose up -d
```
**Utilité:** Lance Gabriel + Ollama (sans Isabelle)

### Démarrer Gabriel + Isabelle
```powershell
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local
docker-compose --profile isabelle up -d
```
**Utilité:** Lance Gabriel + Isabelle + Ollama (configuration complète)

### Démarrer en mode interactif (voir les logs)
```powershell
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local
docker-compose --profile isabelle up
```
**Utilité:** Lance les services ET affiche les logs en continu (Ctrl+C pour arrêter)

### Arrêter tous les services
```powershell
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local
docker-compose down
```
**Utilité:** Arrête tous les conteneurs (Gabriel, Isabelle, Ollama)

### Arrêter un service spécifique
```powershell
docker stop llm-agent-multiloop-run
docker stop isabelle
docker stop ollama
```
**Utilité:** Arrête un conteneur sans arrêter les autres

### Redémarrer Gabriel
```powershell
docker restart llm-agent-multiloop-run
```
**Utilité:** Redémarre Gabriel (utile après modifications)

### Redémarrer tous les services
```powershell
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local
docker-compose restart
```
**Utilité:** Redémarre tous les conteneurs

### Pause/Reprendre les services
```powershell
docker-compose pause
docker-compose unpause
```
**Utilité:** Met en pause/reprend les services (conserve l'état)

---

## SECTION 2: VÉRIFIER L'ÉTAT

### Voir tous les conteneurs en cours d'exécution
```powershell
docker ps
```
**Utilité:** Affiche les conteneurs ACTIFS (Gabriel, Isabelle, Ollama)
**Output:** Montre CONTAINER ID, IMAGE, STATUS, PORTS, NAMES

### Voir TOUS les conteneurs (y compris arrêtés)
```powershell
docker ps -a
```
**Utilité:** Liste tous les conteneurs (actifs + arrêtés)

### Voir le statut détaillé de docker-compose
```powershell
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local
docker-compose ps
```
**Utilité:** Affiche le statut des services (Gabriel, Ollama, Isabelle)

### Vérifier la santé de Gabriel (HTTP API)
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
```
**Utilité:** Vérifie que Gabriel répond sur le port 8000 (API en ligne)
**Output:** `{"status": "online", "service": "Gabriel v4.0", "pipeline": "active"}`

### Vérifier si Ollama est prêt
```powershell
Invoke-WebRequest -Uri "http://localhost:11434" -UseBasicParsing
```
**Utilité:** Vérifie que Ollama (LLM local) tourne sur le port 11434

### Vérifier si Isabelle répond
```powershell
docker ps | findstr isabelle
```
**Utilité:** Vérifie que le conteneur Isabelle tourne

### Voir l'utilisation des ressources en temps réel
```powershell
docker stats
```
**Utilité:** Affiche CPU, mémoire, réseau pour tous les conteneurs (Ctrl+C pour quitter)

---

## SECTION 3: ACCÉDER AUX CONTENEURS

### Accéder au shell de Gabriel (bash)
```powershell
docker exec -it llm-agent-multiloop-run bash
```
**Utilité:** Entre dans le conteneur Gabriel en shell bash
**Puis:** `ls`, `cat`, `python`, etc.

### Accéder au shell de Gabriel en tant qu'utilisateur root
```powershell
docker exec -it -u root llm-agent-multiloop-run bash
```
**Utilité:** Accès root pour installations/modifications

### Accéder au shell d'Isabelle
```powershell
docker exec -it isabelle bash
```
**Utilité:** Entre dans le conteneur Isabelle

### Accéder au shell d'Ollama
```powershell
docker exec -it ollama bash
```
**Utilité:** Entre dans le conteneur Ollama (LLM)

### Exécuter une commande directement (sans shell interactif)
```powershell
docker exec llm-agent-multiloop-run python -c "print('Hello Gabriel')"
```
**Utilité:** Exécute une commande et retourne le résultat

---

## SECTION 4: VOIR LES FICHIERS MONTÉS

### Compter les 100 fichiers Isabelle (.thy)
```bash
docker exec llm-agent-multiloop-run bash -c "ls /theories/projects/*.thy | wc -l"
```
**Output:** `100`

### Compter les 100 fichiers texte (.txt)
```bash
docker exec llm-agent-multiloop-run bash -c "ls /theories/projects/txt/*.txt | wc -l"
```
**Output:** `100`

### Compter les 100 fichiers LaTeX (.tex)
```bash
docker exec llm-agent-multiloop-run bash -c "ls /theories/projects/tex/*.tex | wc -l"
```
**Output:** `100`

### Lister les 10 premiers fichiers (.thy)
```bash
docker exec llm-agent-multiloop-run bash -c "ls /theories/projects/*.thy | head -10"
```

### Lister tous les fichiers d'un dossier
```bash
docker exec llm-agent-multiloop-run bash -c "ls /theories/projects/"
```

### Voir le contenu d'un fichier spécifique
```bash
docker exec llm-agent-multiloop-run bash -c "cat /theories/projects/projet_uni_car_savard_01.thy"
```

### Voir la taille d'un fichier
```bash
docker exec llm-agent-multiloop-run bash -c "du -h /theories/projects/projet_uni_car_savard_01.thy"
```

### Vérifier l'espace disponible
```bash
docker exec llm-agent-multiloop-run bash -c "df -h /theories"
```

### Chercher un fichier
```bash
docker exec llm-agent-multiloop-run bash -c "find /theories -name '*.thy' -type f"
```

---

## SECTION 5: REQUÊTES À GABRIEL (HTTP API)

### Requête simple: Poser une question
```powershell
$body = @{
    question = "Quel est le 10eme nombre premier?"
    source = "powershell"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:8000/query" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body `
  -UseBasicParsing

$response.Content | ConvertFrom-Json | Format-List
```
**Utilité:** Pose une question à Gabriel et affiche la réponse formatée

### Synchroniser avec www.universestaucarre.com
```powershell
$body = @{
    session_id = "session-$(Get-Random)"
    question = "Qu'est-ce que l'univers au carre?"
    results = @{
        gpt4 = "Réponse GPT4"
        claude = "Réponse Claude"
        gemini = "Réponse Gemini"
        gabriel_web = "Réponse Gabriel Web"
    }
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/sync/universestaucarre" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body `
  -UseBasicParsing
```
**Utilité:** Synchronise les résultats des 4 IAs

### Vérifier un résultat Isabelle
```powershell
$body = @{
    theory_file = "/theories/projects/exemple.thy"
    status = "success"
    output = "Verification complete"
    timestamp = "$(Get-Date -Format 'o')"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/isabelle/verify" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body $body `
  -UseBasicParsing
```
**Utilité:** Envoie les résultats Isabelle à Gabriel

---

## SECTION 6: LOGS ET DEBUGGING

### Voir les logs Gabriel (50 dernières lignes)
```powershell
docker logs llm-agent-multiloop-run --tail 50
```

### Voir les logs Gabriel en temps réel
```powershell
docker logs llm-agent-multiloop-run -f
```
**Utilité:** Affiche les logs en continu (Ctrl+C pour arrêter)

### Voir les logs Gabriel depuis une date
```powershell
docker logs llm-agent-multiloop-run --since 2025-01-15T10:00:00
```

### Voir les logs avec timestamps
```powershell
docker logs llm-agent-multiloop-run -t --tail 100
```

### Voir les logs d'Isabelle
```powershell
docker logs isabelle --tail 50
```

### Voir les logs d'Ollama
```powershell
docker logs ollama --tail 50
```

### Sauvegarder les logs dans un fichier
```powershell
docker logs llm-agent-multiloop-run > C:\logs-gabriel.txt
```

### Voir les 1000 dernières lignes
```powershell
docker logs llm-agent-multiloop-run --tail 1000 > C:\full-logs.txt
```

### Monitorer en temps réel (combiné)
```powershell
# Fenêtre 1
docker logs llm-agent-multiloop-run -f

# Fenêtre 2
docker logs isabelle -f

# Fenêtre 3
docker stats llm-agent-multiloop-run
```

---

## SECTION 7: JEDI IT (ISABELLE GUI)

### Accéder à Isabelle
```powershell
docker exec -it isabelle bash
```

### Lancer Jed it (interface GUI)
```bash
# (À taper APRÈS: docker exec -it isabelle bash)
isabelle jedit /theories/projects/projet_uni_car_savard_26.thy
```

### Vérifier un fichier .thy (CLI)
```bash
isabelle process -o quick -T /theories/projects/projet_uni_car_savard_26.thy
```

### Compiler LaTeX en PDF
```bash
cd /theories/projects/tex
pdflatex -interaction=nonstopmode projet_uni_car_savard_26.tex
```

### Afficher le PDF généré
```bash
ls /theories/projects/tex/*.pdf
```

### Lancer plusieurs fichiers dans Jed it
```bash
isabelle jedit /theories/projects/projet_uni_car_savard_*.thy
```

---

## SECTION 8: GESTION DES CONTENEURS

### Supprimer un conteneur arrêté
```powershell
docker stop llm-agent-multiloop-run
docker rm llm-agent-multiloop-run
```

### Supprimer une image
```powershell
docker rmi agent-multiloop-gabriel-local-llm-agent-multiloop
```

### Nettoyer les ressources inutilisées
```powershell
docker system prune -a
```
**ATTENTION:** Supprime images, conteneurs, volumes arrêtés!

### Voir l'espace disque utilisé
```powershell
docker system df
```

### Voir le détail de l'utilisation
```powershell
docker system df -v
```

---

## SECTION 9: RÉSEAU ET PORTS

### Voir tous les ports ouverts
```powershell
netstat -ano
```

### Voir les ports spécifiques
```powershell
netstat -ano | findstr :8000
netstat -ano | findstr :11434
```

### Voir les ports du conteneur Gabriel
```powershell
docker port llm-agent-multiloop-run
```

### Lister les réseaux Docker
```powershell
docker network ls
```

### Inspecter le réseau agent-network
```powershell
docker network inspect agent-network
```

### Voir les conteneurs connectés à un réseau
```powershell
docker network inspect agent-network --format='{{range .Containers}}{{println .Name}}{{end}}'
```

---

## SECTION 10: REBUILD ET IMAGES

### Voir les images disponibles
```powershell
docker images
```

### Rebuilder l'image Gabriel
```powershell
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local
docker-compose build
```

### Rebuilder et relancer
```powershell
docker-compose up -d --build
```

### Rebuilder sans cache
```powershell
docker-compose build --no-cache
```

### Voir l'historique d'une image
```powershell
docker history agent-multiloop-gabriel-local-llm-agent-multiloop
```

---

## SECTION 11: FICHIERS ET VOLUMES

### Lister les volumes
```powershell
docker volume ls
```

### Inspecter un volume
```powershell
docker volume inspect agent-data
```

### Copier depuis conteneur vers host
```powershell
docker cp llm-agent-multiloop-run:/home/agent/app/data C:\backup-data
```

### Copier depuis host vers conteneur
```powershell
docker cp C:\files llm-agent-multiloop-run:/home/agent/app/
```

---

## SECTION 12: SCRIPTS UTILES

### Script: Démarrage complet avec vérification
```powershell
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local
docker-compose --profile isabelle up -d
Write-Host "Attente du démarrage..." -ForegroundColor Cyan
Start-Sleep -Seconds 30

Write-Host "Vérification..." -ForegroundColor Yellow
$health = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
if ($health.StatusCode -eq 200) {
    Write-Host "Gabriel est ONLINE!" -ForegroundColor Green
} else {
    Write-Host "Gabriel ne répond pas" -ForegroundColor Red
}
docker-compose ps
```

### Script: Arrêt propre
```powershell
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local
Write-Host "Arrêt des services..." -ForegroundColor Yellow
docker-compose down
Write-Host "Services arrêtés!" -ForegroundColor Green
```

### Script: Vérifier les 300 templates
```powershell
$thy = [int](docker exec llm-agent-multiloop-run bash -c "ls /theories/projects/*.thy 2>/dev/null | wc -l")
$txt = [int](docker exec llm-agent-multiloop-run bash -c "ls /theories/projects/txt/*.txt 2>/dev/null | wc -l")
$tex = [int](docker exec llm-agent-multiloop-run bash -c "ls /theories/projects/tex/*.tex 2>/dev/null | wc -l")

Write-Host "Templates:" -ForegroundColor Cyan
Write-Host "  .thy: $thy/100"
Write-Host "  .txt: $txt/100"
Write-Host "  .tex: $tex/100"
Write-Host "  TOTAL: $($thy + $txt + $tex)/300" -ForegroundColor Yellow
```

### Script: Monitorer les 3 services
```powershell
Write-Host "Démarrage du monitoring..." -ForegroundColor Cyan

while ($true) {
    Clear-Host
    Write-Host "=== STATUS ===" -ForegroundColor Yellow
    docker-compose ps
    Write-Host ""
    Write-Host "=== RESSOURCES ===" -ForegroundColor Yellow
    docker stats --no-stream
    Start-Sleep -Seconds 5
}
```

---

## SECTION 13: COMMANDES GABRIEL CLI (Interface Interactive)

### Depuis l'interface Gabriel

```
gabriel> aide
```
Affiche le menu d'aide

```
gabriel> commandes
```
Liste toutes les commandes

```
gabriel> Quel est le 26eme nombre premier?
```
Pose une question

```
gabriel> ci
```
Rapport CI/tests

```
gabriel> quitter
```
Quitte Gabriel

---

## RÉSUMÉ DES COMMANDES LES PLUS UTILES

### Top 10 essentielles:

| # | Commande | Utilité |
|---|----------|---------|
| 1 | `docker-compose --profile isabelle up -d` | Démarrer Gabriel + Isabelle |
| 2 | `docker ps` | Voir les conteneurs actifs |
| 3 | `docker logs llm-agent-multiloop-run -f` | Voir les logs en temps réel |
| 4 | `Invoke-WebRequest http://localhost:8000/health` | Vérifier Gabriel (API) |
| 5 | `docker exec -it llm-agent-multiloop-run bash` | Accès shell Gabriel |
| 6 | `docker exec -it isabelle bash` | Accès shell Isabelle |
| 7 | `docker-compose down` | Arrêter tous les services |
| 8 | `docker stats` | Monitorer ressources |
| 9 | `docker compose ps` | État des services |
| 10 | `docker system prune -a` | Nettoyer tout |

---

**Version:** 4.0 - COMMANDES COMPLÈTES ET ÉTENDUES  
**Date:** 2025-01-15  
**Total de sections:** 13  
**Total de commandes:** 150+
