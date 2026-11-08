# GABRIEL v5.0 - MISE À JOUR COMPLÈTE

## 🎯 OBJECTIF

Résoudre le problème du port qui reste occupé même après fermeture de Gabriel.

**Solution**: Fermeture complète de la socket au niveau du système quand Gabriel s'arrête.

---

## 📋 AVANT DE COMMENCER

Vérifiez l'état actuel:

```powershell
docker ps
# → Vous verrez le conteneur llm-agent-multiloop-run
```

---

## ⚡ MISE À JOUR RAPIDE (2 minutes)

### Option 1: Script Automatique (Recommandé)

```powershell
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local

# Exécuter le script de mise à jour
.\UPDATE_GABRIEL_v5.ps1

# Attendre 2-3 minutes (rebuild + restart)
```

**Le script fait automatiquement**:
1. ✅ Arrête tous les conteneurs
2. ✅ Rebuild l'image Docker
3. ✅ Relance Gabriel v5.0
4. ✅ Vérifie que tout fonctionne

### Option 2: Commandes Manuelles

```powershell
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local

# Arrêter les conteneurs
docker compose down -v

# Attendre 10 secondes
Start-Sleep -Seconds 10

# Rebuild l'image
docker compose build --no-cache

# Relancer
docker compose up -d
```

---

## ✅ VÉRIFICATION

Après la mise à jour, vérifiez que Gabriel v5.0 tourne:

```powershell
docker logs llm-agent-multiloop-run | tail -20

# Vous devriez voir:
# [INIT] Starting Gabriel v5.0 (Multi-Loop Mathematical Agent)
```

---

## 🚀 UTILISATION

### Démarrer Gabriel

```powershell
.\gabriel.ps1 start

# Attendre 20 secondes
# Accéder à: http://localhost:8080
```

### Arrêter Gabriel (IMPORTANT)

**Option 1**: Taper "quitter" dans Gabriel
```
gabriel> quitter
```

**Option 2**: Ctrl+C dans le terminal

**Option 3**: Utiliser le script
```powershell
.\gabriel.ps1 stop
```

### APRÈS l'arrêt, vérifiez que le port est libre

```powershell
netstat -ano | findstr :8080

# Résultat:
# - VIDE = SUCCESS! ✅
# - Si encore occupé = Attendre 5 secondes
```

---

## 🔍 QU'EST-CE QUI A CHANGÉ?

### Fichiers Nouveaux:
- `socket_cleanup.py` - Librairie pour fermer complètement la socket

### Fichiers Modifiés:
- `main_cli.py` - Nouvelle version v5.0 avec cleanup

### Comment ça fonctionne:
1. Quand Gabriel démarre: crée une socket TCP sur port 8080
2. Quand Gabriel s'arrête: **ferme COMPLÈTEMENT la socket** au niveau système
3. Port 8080 devient immédiatement disponible
4. Docker Desktop n'est JAMAIS affecté

---

## ⚠️ IMPORTANT

### Ces actions sont INTERDITES:
```powershell
# ❌ NE PAS FAIRE:
taskkill /PID 25988 /F

# ❌ NE PAS FAIRE:
Get-Process docker* | Stop-Process

# ❌ NE PAS FAIRE:
Fermer PowerShell sans taper "quitter"
```

### À FAIRE:
```powershell
# ✅ À FAIRE:
.\gabriel.ps1 stop
# OU
Ctrl+C
# OU
Taper "quitter" dans Gabriel
```

---

## 🧪 TEST COMPLET

Après mise à jour, testez la nouvelle fonctionnalité:

```powershell
# 1. Démarrer
.\gabriel.ps1 start
# Attendre 20 sec

# 2. Vérifier que le port est occupé
netstat -ano | findstr :8080
# Résultat: PID occupé ✅

# 3. Accéder
http://localhost:8080

# 4. Utiliser Gabriel...

# 5. Arrêter (taper dans Gabriel):
quitter

# 6. Attendre 5 secondes

# 7. Vérifier que le port est LIBRE
netstat -ano | findstr :8080
# Résultat: VIDE ✅

# 8. Redémarrer immédiatement:
.\gabriel.ps1 start
# Devrait démarrer sans "Port already allocated"!
```

---

## 📊 RÉSULTAT ATTENDU

```
AVANT (v4.0):
  Taper "quitter"
  ❌ "Port 8080 already allocated"
  ❌ Redémarrage impossible sans Docker Desktop restart
  
APRÈS (v5.0):
  Taper "quitter"
  ✅ Port se libère immédiatement
  ✅ Redémarrage instantané possible
  ✅ Docker Desktop jamais affecté
```

---

## 🆘 TROUBLESHOOTING

### Erreur: "docker compose build" échoue

**Solution**:
```powershell
docker system prune -a --volumes
docker compose up -d
```

### Erreur: "Port 8080 still allocated"

**Solution**:
```powershell
# Attendre 10 secondes
Start-Sleep -Seconds 10

# Vérifier l'état
netstat -ano | findstr :8080

# Redémarrer
docker compose restart
```

### Gabriel ne démarre pas après mise à jour

**Solution**:
```powershell
# Voir les logs
docker logs llm-agent-multiloop-run

# Redémarrer complètement
docker compose down -v
docker compose up -d
```

---

## ✨ STATUS FINAL

- ✅ Socket cleanup implémenté
- ✅ Signal handlers configurés
- ✅ Port se libère proprement
- ✅ Docker Desktop protégé
- ✅ Production-ready

**Gabriel v5.0 est prêt!** 🚀

---

## 📞 COMMANDES RAPIDES

| Action | Commande |
|--------|----------|
| Mise à jour | `.\UPDATE_GABRIEL_v5.ps1` |
| Démarrer | `.\gabriel.ps1 start` |
| Arrêter | `.\gabriel.ps1 stop` |
| Logs | `docker logs llm-agent-multiloop-run` |
| Vérifier port | `netstat -ano | findstr :8080` |
| Restart complet | `docker compose down -v ; docker compose up -d` |

---

*Gabriel v5.0 - Socket Cleanup Complete* ✅
