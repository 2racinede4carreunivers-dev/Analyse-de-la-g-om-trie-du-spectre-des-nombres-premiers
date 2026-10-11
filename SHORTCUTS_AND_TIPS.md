# GABRIEL v5.4 - RACCOURCIS ET ASTUCES

## 🎯 RACCOURCIS WINDOWS

### Créer des Raccourcis Bureau

Pour lancer Gabriel directement depuis le Bureau:

#### 1. Raccourci "Démarrer Gabriel"

- Clic droit sur le Bureau → Nouveau → Raccourci
- Emplacement: 
  ```
  powershell -NoExit -ExecutionPolicy Bypass -File "C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local\gabriel.ps1" start
  ```
- Nom: "Démarrer Gabriel"
- Clic droit → Propriétés → "Exécuter en tant qu'administrateur" (cocher)
- OK

Double-cliquez pour démarrer Gabriel!

#### 2. Raccourci "Arrêter Gabriel"

- Clic droit sur le Bureau → Nouveau → Raccourci
- Emplacement:
  ```
  powershell -NoExit -ExecutionPolicy Bypass -File "C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local\gabriel.ps1" stop
  ```
- Nom: "Arrêter Gabriel"
- OK

#### 3. Raccourci "Statut Gabriel"

- Clic droit sur le Bureau → Nouveau → Raccourci
- Emplacement:
  ```
  powershell -NoExit -ExecutionPolicy Bypass -File "C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local\gabriel.ps1" status
  ```
- Nom: "Statut Gabriel"
- OK

---

## ⌨️ COMMANDES POWERSHELL RAPIDES

### Depuis PowerShell ISE

```powershell
# Aller au dossier Gabriel
cd C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local

# Démarrer
.\gabriel.ps1 start

# Dans une autre PowerShell:
# Vérifier statut
.\gabriel.ps1 status

# Arrêter
.\gabriel.ps1 stop
```

---

## 🖱️ FICHIERS .BAT (Double-clic)

Utilisez directement:

- `START_GABRIEL.bat` → Démarre Gabriel
- `STOP_GABRIEL.bat` → Arrête Gabriel

Double-cliquez le fichier .bat que vous voulez exécuter!

---

## 📱 ACCÈS GABRIEL

```
URL: http://localhost:8080
```

Bookmark cette URL dans votre navigateur pour accès rapide!

---

## 🔧 COMMANDES RAPIDES POWERSHELL

```powershell
# Vérifier que port 8080 est libre
netstat -ano | findstr :8080
# (vide = libre, occupé = erreur)

# Vérifier Docker
docker ps
# (montre les conteneurs actifs)

# Voir logs Gabriel
docker logs llm-agent-multiloop-run

# Redémarrer Gabriel
.\gabriel.ps1 restart

# Tous les statuts
.\gabriel.ps1 status
```

---

## 💡 ASTUCES

### 1. Créer un Alias PowerShell

Ajouter à votre profil PowerShell:

```powershell
# Ouvrir:
notepad $PROFILE

# Ajouter:
Set-Alias -Name g-start -Value "C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local\gabriel.ps1 start"
Set-Alias -Name g-stop -Value "C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local\gabriel.ps1 stop"
Set-Alias -Name g-status -Value "C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local\gabriel.ps1 status"

# Sauvegarder (Ctrl+S)
```

Puis utiliser:
```powershell
g-start    # Démarre Gabriel
g-stop     # Arrête Gabriel
g-status   # Voir statut
```

### 2. Créer une Fonction PowerShell

```powershell
# Ajouter à votre profil:
function gabriel {
    param($cmd = "status")
    & "C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local\gabriel.ps1" $cmd
}

# Utiliser:
gabriel start    # Démarre
gabriel stop     # Arrête
gabriel status   # Statut
```

### 3. Ajout Menu Contexte Windows

Créer `Add-ContextMenu.ps1`:

```powershell
$path = "C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local"
reg add "HKCU\Software\Classes\Directory\Background\shell\Gabriel Start" /v Icon /d "powershell.exe"
reg add "HKCU\Software\Classes\Directory\Background\shell\Gabriel Start\command" /d "powershell -ExecutionPolicy Bypass -File $path\gabriel.ps1 start"
```

Puis clic droit sur le bureau → "Gabriel Start"

---

## 🎓 WORKFLOW OPTIMISÉ

### Démarrage Rapide

1. Double-cliquez `START_GABRIEL.bat`
2. Attendez 20 secondes
3. Ouvrir navigateur: `http://localhost:8080`
4. Utiliser Gabriel

### Arrêt Rapide

1. Double-cliquez `STOP_GABRIEL.bat`
2. Attendre confirmation
3. Fermer fenêtre

### Redémarrage Rapide

1. Double-cliquez `STOP_GABRIEL.bat`
2. Attendre 5 secondes
3. Double-cliquez `START_GABRIEL.bat`

---

## 📌 RACCOURCIS À MÉMORISER

| Action | Commande | Type |
|--------|----------|------|
| Démarrer | `.\gabriel.ps1 start` | PowerShell |
| Arrêter | `.\gabriel.ps1 stop` | PowerShell |
| Redémarrer | `.\gabriel.ps1 restart` | PowerShell |
| Statut | `.\gabriel.ps1 status` | PowerShell |
| Démarrer | Double-clic `START_GABRIEL.bat` | Batch |
| Arrêter | Double-clic `STOP_GABRIEL.bat` | Batch |

---

## ✨ SETUP RECOMMANDÉ

1. Créer raccourcis Bureau pour Start/Stop
2. Bookmark http://localhost:8080 dans navigateur
3. Ajouter alias PowerShell si vous utilisez souvent CLI
4. Configurer "Exécuter en tant qu'administrateur" pour les .bat

---

## 🎯 RÉSUMÉ

**Façon Plus Rapide**: Double-clic sur `START_GABRIEL.bat`
**Façon Plus Flexible**: PowerShell `.\gabriel.ps1 start`
**Façon Plus Automatisée**: Alias ou fonction PowerShell

---

*Choisissez la méthode qui vous convient le mieux!* 🚀
