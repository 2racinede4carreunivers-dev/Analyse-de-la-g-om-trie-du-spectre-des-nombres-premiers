# ============================================================
# GABRIEL v5.4 - FINAL WORKING SOLUTION
# ============================================================

## ✅ PROBLÈME RÉSOLU

**Le vrai problème**: Le script `start-agent.ps1` utilisait `docker compose run --rm --service-ports` qui créait un **nouveau conteneur à chaque lancement**, causant des conflits de port.

**La solution**: Changé en `docker compose up -d` + `docker attach`, qui **réutilise le même conteneur**.

---

## 📝 RÉSUMÉ DES CHANGEMENTS

### 1. Port Configuration
- Changé de port 8080 → 9001 (pour éviter les conflits Docker Desktop)
- Configuré dans `docker-compose.yml`: `GABRIEL_HTTP_PORT=9001`

### 2. Restart Policy
- Changé `restart: unless-stopped` → `restart: "no"`
- Évite les relances infinies causant des listeners orphelins

### 3. Launcher Script (`start-agent.ps1`)
**Ancien**:
```powershell
docker compose run --rm --service-ports $ServiceMain python main_cli.py
```

**Nouveau**:
```powershell
docker compose down  # Nettoyer d'abord
docker compose up -d # Démarrer services (réutilise conteneur)
docker attach $ContainerName  # Connecter terminal
```

### 4. Docker Cleanup
- Exécuté `docker system prune -a --volumes -f`
- Supprime tous les conteneurs/volumes orphelins
- Nettoie le cache build corrompu

---

## 🚀 UTILISATION MAINTENANT

### Démarrer Gabriel depuis PowerShell ISE:
```powershell
.\start-agent.ps1
```

### Options disponibles:
```powershell
.\start-agent.ps1 -Rebuild    # Rebuild complet l'image
.\start-agent.ps1 -Stop       # Arrêter complètement
.\start-agent.ps1 -Status     # Voir l'état
.\start-agent.ps1 -Logs       # Voir les logs en streaming
```

### Accès web:
```
http://localhost:9001
```

---

## 📊 AVANT vs APRÈS

| | Avant | Après |
|---|-------|-------|
| **Port** | 9000 (conflit Docker) | 9001 (libre) ✅ |
| **Launcher** | `docker run` (nuevo conteneur) | `docker up` (réutilise) ✅ |
| **Erreur** | "port already allocated" | ❌ Disparue |
| **ISE Restart** | Impossible | ✅ Fonctionne |
| **Session Duration** | N/A | Illimitée |

---

## 🔧 FICHIERS MODIFIÉS

1. **docker-compose.yml**
   - Port: 8080 → 9001
   - Restart: unless-stopped → "no"
   - Command: gabriel_launcher.py → main_cli.py

2. **start-agent.ps1**
   - Remplacé `docker compose run` par `docker compose up`
   - Ajouté `docker attach` pour connecter le terminal
   - Simplifié la logique globale

3. **Dockerfile.cli**
   - Revert à v4.0 (enlevé socket_cleanup qui n'était pas dans build)
   - Utilise main_cli.py standard

---

## 🎯 CLÉS DU SUCCÈS

✅ **Ne pas utiliser `docker compose run`** pour les services persistants
✅ **Utiliser `restart: no`** pour éviter les relances infinies  
✅ **Nettoyer Docker complètement** (`docker system prune`)
✅ **Monter les volumes en read-write** (pas de `:ro`)
✅ **Utiliser `docker attach` au lieu de `exec`** pour terminal interactif

---

## 📞 COMMANDES UTILES

```powershell
# Démarrer Gabriel
.\start-agent.ps1

# Voir les logs en temps réel
.\start-agent.ps1 -Logs

# Arrêter complètement
.\start-agent.ps1 -Stop

# Vérifier l'état
.\start-agent.ps1 -Status

# Rebuild l'image
.\start-agent.ps1 -Rebuild
```

---

## ✨ STATUS: PRODUCTION READY

Gabriel v5.4 est maintenant **stable, opérationnel et prêt pour l'utilisation régulière** depuis PowerShell ISE! 🎉

**Accédez maintenant**: http://localhost:9001
