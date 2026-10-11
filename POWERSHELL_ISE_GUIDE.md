# ✅ GABRIEL POWERSHELL ISE - GUIDE COMPLET

## 🎯 LE VRAI PROBLÈME

Quand vous lancez Gabriel depuis PowerShell ISE et que vous fermez le terminal:
1. ❌ Les conteneurs Docker restent actifs
2. ❌ Le port 8080 reste occupé par Docker
3. ❌ Tuer le processus = **Ferme Docker Desktop**

## ✅ LA VRAIE SOLUTION

**Ne pas tuer le processus. Arrêter proprement les conteneurs.**

---

## 🚀 UTILISATION AVEC POWERSHELL ISE

### Démarrage de Gabriel

**Dans PowerShell ISE, exécutez:**

```powershell
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local

# Démarrer Gabriel
.\gabriel.ps1 start

# Attendre 20 secondes que Gabriel soit complètement chargé
# Puis accéder à http://localhost:8080
```

**Ce que fait le script:**
- ✅ Vérifie que le port 8080 est libre
- ✅ Lance `docker compose up -d`
- ✅ Attend 20 secondes que Gabriel démarre
- ✅ Affiche le statut

### Arrêt de Gabriel

**IMPORTANT: Ne fermez PAS simplement PowerShell ISE!**

**À la place, dans le même terminal:**

```powershell
# Arrêt propre
.\gabriel.ps1 stop
```

**Ce que fait le script:**
- ✅ Lance `docker compose down`
- ✅ Attend que les conteneurs s'arrêtent
- ✅ Libère le port 8080
- ✅ Affiche la confirmation

### Autres Commandes

```powershell
# Voir le statut
.\gabriel.ps1 status

# Redémarrer complètement
.\gabriel.ps1 restart

# Voir les logs
.\gabriel.ps1 logs
```

---

## ⚠️ IMPORTANT: NE JAMAIS FAIRE

```powershell
# ❌ NE FAITES PAS:
taskkill /PID 25988 /F
# → Cela ferme Docker Desktop!

# ❌ NE FAITES PAS:
Get-Process docker* | Stop-Process
# → Cela ferme Docker Desktop!

# ❌ NE FAITES PAS:
Fermer simplement PowerShell ISE
# → Les conteneurs restent actifs et gardent le port
```

---

## ✅ WORKFLOW COMPLET

### Scénario 1: Première Utilisation

```powershell
# 1. Ouvrir PowerShell ISE
# 2. Exécuter:
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local
.\gabriel.ps1 start

# 3. Attendre 20 secondes
# 4. Accéder à http://localhost:8080
# 5. Utiliser Gabriel...

# 6. Quand terminé:
.\gabriel.ps1 stop

# 7. Attendre confirmation
# 8. Fermer PowerShell ISE si désiré
```

### Scénario 2: Redémarrage

```powershell
# Gabriel tourne déjà, vous voulez le redémarrer:
.\gabriel.ps1 restart

# Cela arrête tout et relance proprement
```

### Scénario 3: Vérifier le Statut

```powershell
# Voir l'état actuel:
.\gabriel.ps1 status

# Affiche:
# ✓ Docker Desktop: RUNNING
# ✓ Gabriel Container: RUNNING
# ✓ Port 8080: LIBRE
```

---

## 🐛 TROUBLESHOOTING

### Erreur: "Port 8080 already allocated"

**Cause**: Port encore occupé par Gabriel précédent

**Solution**:
```powershell
# ✅ Correct:
.\gabriel.ps1 stop          # Arrêt propre
Start-Sleep -Seconds 5      # Attendre 5 secondes
.\gabriel.ps1 start         # Relancer

# ❌ Incorrect:
taskkill /PID ...          # Ne pas tuer!
```

### Erreur: "Docker Desktop not responding"

**Cause**: Docker Desktop s'est fermé

**Solution**:
```powershell
# Relancer Docker Desktop manuellement
# Puis:
.\gabriel.ps1 start
```

### Gabriel ne répond pas sur http://localhost:8080

**Cause**: Délai de démarrage trop court

**Solution**:
```powershell
# Attendre 30 secondes au lieu de 20
Start-Sleep -Seconds 30

# Ou voir les logs:
.\gabriel.ps1 logs
```

---

## 📊 COMPARAISON AVANT/APRÈS

| Situation | Avant (Problématique) | Après (Script) |
|-----------|----------------------|----------------|
| **Démarrage** | Manuel docker compose | `.\gabriel.ps1 start` |
| **Arrêt** | Fermer ISE → port bloqué | `.\gabriel.ps1 stop` |
| **Port occupé** | Doit tuer le processus (ferme Docker!) | Script gère automatiquement |
| **Redémarrage** | Complexe et dangereux | `.\gabriel.ps1 restart` |
| **Fiabilité** | ❌ Instable | ✅ Stable |

---

## 🔐 FICHIERS FOURNIS

| Fichier | Purpose |
|---------|---------|
| `gabriel.ps1` | **Utiliser ceci!** Script PowerShell pour tout contrôler |
| `port-locker.ps1` | Utilitaire avancé (optionnel) |
| `gabriel_control.py` | Alternative Python (optionnel) |

---

## 💡 ASTUCE: Créer un Raccourci

Vous pouvez créer un raccourci Windows qui lance Gabriel directement:

**Créer un fichier `start-gabriel.bat`:**
```batch
@echo off
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local
powershell -ExecutionPolicy Bypass -File gabriel.ps1 start
pause
```

**Double-cliquez pour démarrer Gabriel directement!**

---

## 🎓 RÉSUMÉ EN UNE PHRASE

**Au lieu de combattre Docker, utilisez les scripts PowerShell pour commander Docker proprement.**

---

## ✨ STATUS: READY FOR POWERSHELL ISE

Vous pouvez maintenant:
- ✅ Démarrer Gabriel sans souci
- ✅ L'arrêter proprement
- ✅ Le redémarrer sans port conflict
- ✅ Fermer PowerShell ISE sans risque

**Accès**: http://localhost:8080

**Script**: `.\gabriel.ps1 start|stop|restart|status|logs`

*Plus de problème de port! Plus de fermeture Docker! 🎉*
