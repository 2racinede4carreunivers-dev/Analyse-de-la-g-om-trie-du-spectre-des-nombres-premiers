#!/usr/bin/env powershell
# =============================================================================
#  start-agent.ps1 v4.1 
# =============================================================================

param(
    [switch]$Rebuild,
    [switch]$Logs,
    [switch]$Stop,
    [switch]$Status,
    [switch]$WithIsabelle,
    [switch]$PullOnly
)

Set-Location -Path $PSScriptRoot

$ProjectRoot   = $PSScriptRoot
$ProjectName   = "agent-multiloop-gabriel-local"
$ContainerName = "llm-agent-multiloop-run"
$ServiceMain   = "llm-agent-multiloop"
$ComposeFile   = Join-Path $ProjectRoot "docker-compose.yml"

$C_OK = "Green"; $C_WARN = "Yellow"; $C_ERR = "Red"; $C_INFO = "Cyan"

function Write-Step { param([string]$M) Write-Host "`n>  $M" -ForegroundColor $C_INFO }
function Write-OK   { param([string]$M) Write-Host "   OK  $M" -ForegroundColor $C_OK }
function Write-Warn { param([string]$M) Write-Host "   !!  $M" -ForegroundColor $C_WARN }
function Write-Err  { param([string]$M) Write-Host "   XX  $M" -ForegroundColor $C_ERR }

# ============================================================
# BANNER
# ============================================================
Clear-Host
Write-Host @"

  +============================================================+
  |   MULTI-LOOP MATH AGENT  -  Gabriel Local Launcher  v4.1  |
  |   Methode Spectrale  *  Ollama / OpenAI  *  Isabelle/HOL  |
  +============================================================+

"@ -ForegroundColor Magenta

Write-OK "Project root : $ProjectRoot"

# ============================================================
# Actions rapides
# ============================================================
if ($Stop) {
    Write-Step "Arret complet"
    docker compose -f $ComposeFile -p $ProjectName down -v
    Write-OK "Services arretes et volumes nettoyes."
    exit 0
}

if ($Status) {
    Write-Step "Etat des conteneurs"
    docker compose -f $ComposeFile -p $ProjectName ps
    exit 0
}

if ($Logs) {
    Write-Step "Streaming logs (Ctrl+C pour quitter)"
    docker compose -f $ComposeFile -p $ProjectName logs -f
    exit 0
}

# ============================================================
# Build
# ============================================================
Write-Step "Construction des images"
if ($Rebuild) {
    docker compose -f $ComposeFile -p $ProjectName build --no-cache 2>&1 | Out-Null
} else {
    docker compose -f $ComposeFile -p $ProjectName build 2>&1 | Out-Null
}
if ($LASTEXITCODE -ne 0) { Write-Err "Build echoue"; exit 1 }
Write-OK "Build complete"

# ============================================================
# Up services
# ============================================================
Write-Step "Demarrage des services"
docker compose -f $ComposeFile -p $ProjectName down 2>&1 | Out-Null
docker compose -f $ComposeFile -p $ProjectName up -d ollama ollama-init $ServiceMain 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) { Write-Err "Up echoue"; exit 1 }
Write-OK "Services demarre"

Write-Step "Attente du demarrage complet (15 secondes)"
Start-Sleep -Seconds 15

# ============================================================
# Afficher le statut des conteneurs
# ============================================================
Write-Step "Statut des conteneurs"
docker compose -f $ComposeFile -p $ProjectName ps
Write-OK "Tous les services sont actifs"

# ============================================================
# Afficher les informations de configuration
# ============================================================
Write-Step "Configuration Gabriel"
Write-Host "   Project   : $ProjectName" -ForegroundColor Cyan
Write-Host "   Container : $ContainerName" -ForegroundColor Cyan
Write-Host "   Compose   : $ComposeFile" -ForegroundColor Cyan
Write-Host "   Port HTTP : 9001" -ForegroundColor Cyan

# ============================================================
# Créer le script pour le nouveau terminal
# ============================================================
$terminalScript = @"
# Terminal Gabriel - Session Interactive
Set-Location -Path '$ProjectRoot'

Clear-Host
Write-Host ''
Write-Host '  +===========================================================+' -ForegroundColor Magenta
Write-Host '  |   AGENT MULTI-LOOP  -  Gabriel  |  Terminal actif        |' -ForegroundColor Magenta
Write-Host '  |   Container : $ContainerName' -ForegroundColor Magenta
Write-Host '  |   Mode      : Multi-Loop (Ollama/OpenAI + HOL)            |' -ForegroundColor Magenta
Write-Host '  +===========================================================+' -ForegroundColor Magenta
Write-Host ''
Write-Host '  [Session de travail Gabriel]' -ForegroundColor Yellow
Write-Host '  Tapez : aide, commandes, ask <question>, ou quitter' -ForegroundColor Cyan
Write-Host ''

# Afficher TOUS les logs du conteneur (informations complètes)
Write-Host '  [Logs complets de démarrage Gabriel...]' -ForegroundColor Yellow
Write-Host ''
docker compose -f '$ComposeFile' -p '$ProjectName' logs

Write-Host ''
Write-Host '  [Connexion au terminal interactif Gabriel...]' -ForegroundColor Yellow
Write-Host ''

# Attacher au conteneur
docker attach $ContainerName

# Après quitter
Write-Host ''
Write-Host '  [Session Gabriel terminee]' -ForegroundColor Yellow
Write-Host ''
"@

# Encoder le script pour l'exécuter dans le nouveau terminal
$encoded = [Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($terminalScript))

# ============================================================
# Ouvrir le terminal PowerShell séparé
# ============================================================
Write-Step "Ouverture du terminal Gabriel"
Write-Host "   Lancement d'un terminal PowerShell independant..." -ForegroundColor Yellow

$wt = Get-Command "wt.exe" -ErrorAction SilentlyContinue
if ($wt) {
    Write-OK "Utilisation de Windows Terminal"
    Start-Process "wt.exe" -ArgumentList "powershell -NoExit -EncodedCommand $encoded"
} else {
    Write-OK "Utilisation de PowerShell standard"
    Start-Process "powershell" -ArgumentList "-NoExit -EncodedCommand $encoded"
}

Write-Host ""
Write-Host "==================================================" -ForegroundColor Magenta
Write-Host "  MULTI-LOOP AGENT  -  Session lancee"          -ForegroundColor Green
Write-Host "     Projet   : $ProjectName"                    -ForegroundColor Cyan
Write-Host "     URL Web  : http://localhost:9001"           -ForegroundColor Cyan
Write-Host ""
Write-Host "  Commandes utiles (dans ce terminal) :"          -ForegroundColor Cyan
Write-Host "     .\start-agent.ps1 -Logs      # streaming logs"  -ForegroundColor DarkCyan
Write-Host "     .\start-agent.ps1 -Status    # etat services"   -ForegroundColor DarkCyan
Write-Host "     .\start-agent.ps1 -Stop      # arret complet"    -ForegroundColor DarkCyan
Write-Host "==================================================" -ForegroundColor Magenta
Write-Host ""
Write-Host "  Un nouveau terminal PowerShell a ete ouvert avec Gabriel!" -ForegroundColor Green
Write-Host ""
