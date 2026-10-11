# GABRIEL avec PowerShell ISE - Diagramme de Flux

## AVANT (Problématique)

```
PowerShell ISE
    |
    | docker compose up -d
    v
┌─────────────────────────┐
│ Gabriel Container       │ → Port 8080
│ (llm-agent-multiloop)   │
└─────────────────────────┘

Fermer PowerShell ISE
    |
    ❌ PROBLÈME:
    | - Container reste actif
    | - Port 8080 reste occupé
    | - Suivant: "Port already allocated"
    v
Docker Desktop Backend occupe 8080
    |
    ❌ Essayer: taskkill /PID
    |
    v
    ❌❌❌ Docker Desktop se ferme!
```

---

## APRÈS (Solution)

```
PowerShell ISE
    |
    | .\gabriel.ps1 start
    v
┌────────────────────────────────┐
│ gabriel.ps1                    │
│ ├─ Vérifie port 8080 libre    │
│ ├─ docker compose up -d        │
│ └─ Attends 20 secondes         │
└────────────────────────────────┘
    |
    v
┌─────────────────────────┐
│ Gabriel Container       │ → Port 8080
│ (llm-agent-multiloop)   │
└─────────────────────────┘
    |
    | http://localhost:8080 ✓
    v
    Gabriel fonctionne!

Terminé, executer:
    |
    | .\gabriel.ps1 stop
    v
┌────────────────────────────────┐
│ gabriel.ps1                    │
│ ├─ docker compose down          │
│ └─ Attend stabilisation         │
└────────────────────────────────┘
    |
    v
Port 8080 LIBRE ✓
Docker Desktop INTACT ✓
    |
    v
Fermer PowerShell ISE sans risque! ✓
```

---

## COMMANDES RAPIDES

```
DÉMARRER:
  .\gabriel.ps1 start
  
  ↓ Attendre 20 secondes
  
  → http://localhost:8080


VÉRIFIER STATUS:
  .\gabriel.ps1 status
  
  Affiche:
  ✓ Docker: ACTIF
  ✓ Gabriel: ACTIF  
  ✓ Port 8080: LIBRE


ARRÊTER:
  .\gabriel.ps1 stop
  
  → Port 8080 LIBRE


REDÉMARRER:
  .\gabriel.ps1 restart
  
  = stop + start automatique
```

---

## PORT ALLOCATION

```
AVANT (Port 9000):
  Windows    Docker Backend    Gabriel
    9000  ←→ occupé ←→ (conflit!)

APRÈS (Port 8080):
  Windows    Docker Backend    Gabriel
    8080  ←→ libre ←→ 8000 (interne)
             (ne l'utilise pas)
```

---

## RÉSUMÉ VISUEL

```
Start: .\gabriel.ps1 start
  ✓ Port libre?
  ✓ Docker compose up
  ✓ Attendre
  ✓ Accès http://localhost:8080

Stop: .\gabriel.ps1 stop
  ✓ Docker compose down
  ✓ Port libéré
  ✓ Docker Desktop intact

Restart: .\gabriel.ps1 restart
  = Start → Stop → Start
```

---

## FICHIERS CLÉS

```
C:\agent-multiloop-Gabriel-local-final\
  agent-multiloop-Gabriel-local\
    ├─ gabriel.ps1 ← UTILISER CECI!
    ├─ docker-compose.yml (port: 8080)
    ├─ GABRIEL_FINAL_SOLUTION.txt ← Lire ceci
    └─ theories/
         └─ tex/
              └─ Geometrie_du_Spectre_des_Nombres_Premiers_2026.pdf ✓
```

---

**STATUS: ✅ PRÊT À UTILISER**

Lancez simplement: `.\gabriel.ps1 start`
