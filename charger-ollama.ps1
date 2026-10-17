#!/usr/bin/env powershell
# =============================================================================
#  charger-ollama.ps1 — Charge et verifie le LLM Ollama pour
#  << La fiancee de Cline Mm. Gabriel multiloop local >>
#
#  Role :
#    1. Verifie que Docker Desktop tourne
#    2. Verifie/demarre le conteneur Ollama (via docker-compose)
#    3. Teste l'API Ollama (/api/version + /api/tags sur le port 11434)
#    4. S'assure que le modele (defaut llama3.2) est present (pull si absent)
#    5. (-Preload) precharge le modele en memoire (evite la latence du 1er appel)
#    6. (-StartAgent) enchaine sur le demarrage de l'agent Gabriel
#
#  Usage :
#    .\charger-ollama.ps1                 # verifie + charge le modele
#    .\charger-ollama.ps1 -Preload        # + precharge le modele en RAM
#    .\charger-ollama.ps1 -Model mistral  # charge un autre modele
#    .\charger-ollama.ps1 -StartAgent     # + demarre Gabriel a la fin
#
#  NB : Ollama natif Windows peut AUSSI occuper le port 11434. Ce script pilote
#       le conteneur Docker 'ollama' (celui que l'agent utilise en interne via
#       le reseau Docker : http://ollama:11434). Si le natif bloque le port,
#       fermez l'app Ollama Windows puis relancez.
# =============================================================================

param(
    [string]$Model = "llama3.2",
    [switch]$Preload,
    [switch]$StartAgent
)

# --- Racine du projet (derivee du script, comme start-agent.ps1) ---
$ProjectRoot = $PSScriptRoot
$ComposeFile = Join-Path $ProjectRoot "docker-compose.yml"
$ProjectName = "analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers"
$ServiceMain = "llm-agent-multiloop"
$ContainerName = "llm-agent-multiloop-run"

$C_OK = "Green"; $C_WARN = "Yellow"; $C_ERR = "Red"; $C_INFO = "Cyan"

function Write-Step { param([string]$M) Write-Host "`n>  $M" -ForegroundColor $C_INFO }
function Write-OK   { param([string]$M) Write-Host "   OK  $M" -ForegroundColor $C_OK }
function Write-Warn { param([string]$M) Write-Host "   !!  $M" -ForegroundColor $C_WARN }
function Write-Err  { param([string]$M) Write-Host "   XX  $M" -ForegroundColor $C_ERR }

Write-Host @"

  +============================================================+
  |   CHARGEMENT OLLAMA  -  La fiancee de Cline Mm. Gabriel    |
  |   LLM local primaire  *  modele : $Model
  +============================================================+

"@ -ForegroundColor Magenta

# --- 1. Docker actif ? ---
Write-Step "Verification de Docker Desktop"
docker info *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Err "Docker Desktop ne repond pas."
    Write-Warn "Action : demarrez Docker Desktop puis relancez ce script."
    exit 1
}
Write-OK "Docker Desktop : actif"

# --- 2. Conteneur Ollama ---
Write-Step "Verification du conteneur Ollama"
$running = docker ps --filter "name=^/ollama$" --format "{{.Names}}"
if (-not $running) {
    Write-Warn "Conteneur 'ollama' arrete -> demarrage via docker compose..."
    docker compose -f $ComposeFile -p $ProjectName up -d ollama *> $null
    if ($LASTEXITCODE -ne 0) { Write-Err "Echec du demarrage d'Ollama"; exit 1 }
    Write-OK "Attente du demarrage d'Ollama (10s)..."
    Start-Sleep -Seconds 10
} else {
    Write-OK "Conteneur 'ollama' : en cours d'execution"
}

# --- 3. API Ollama ---
Write-Step "Test de l'API Ollama (port 11434)"
try {
    $ver = (Invoke-WebRequest -Uri "http://localhost:11434/api/version" -UseBasicParsing -TimeoutSec 5).Content
    Write-OK "API Ollama repond : $ver"
} catch {
    Write-Err "API Ollama injoignable sur http://localhost:11434"
    Write-Warn "Verifiez : docker logs --tail 20 ollama"
    exit 1
}

# --- 4. Modele present ? ---
Write-Step "Verification du modele '$Model'"
try {
    $tags = (Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -UseBasicParsing -TimeoutSec 5).Content | ConvertFrom-Json
    $names = $tags.models | ForEach-Object { $_.name }
} catch {
    Write-Err "Impossible de lister les modeles : $($_.Exception.Message)"
    exit 1
}
if ($names | Where-Object { $_ -like "$Model*" }) {
    Write-OK "Modele deja present : $($names -join ', ')"
} else {
    Write-Warn "Modele '$Model' absent -> telechargement (plusieurs minutes possibles)..."
    docker exec ollama ollama pull $Model
    if ($LASTEXITCODE -ne 0) { Write-Err "Echec du pull du modele '$Model'"; exit 1 }
    Write-OK "Modele '$Model' telecharge"
}

# --- 5. Prechargement (option) ---
if ($Preload) {
    Write-Step "Prechargement du modele en memoire (warm-up)..."
    docker exec ollama ollama run $Model "Reponds uniquement : OK" 2>&1 | Select-Object -Last 1
    Write-OK "Modele precharge"
}

# --- 6. Resume + demarrage agent (option) ---
Write-Step "Resume"
Write-Host "   Ollama  : http://localhost:11434 (modele $Model)" -ForegroundColor Cyan
Write-Host "   Agent   : le conteneur Gabriel se connecte au reseau Docker interne" -ForegroundColor Cyan
Write-Host "             via http://ollama:11434 (variable OLLAMA_HOST du .env)" -ForegroundColor Cyan

if ($StartAgent) {
    Write-Step "Demarrage de l'agent Gabriel..."
    docker compose -f $ComposeFile -p $ProjectName up -d $ServiceMain *> $null
    if ($LASTEXITCODE -eq 0) {
        Write-OK "Agent demarre."
        Write-Host "     CLI interactif : docker attach $ContainerName" -ForegroundColor Cyan
        Write-Host "     HTTP API       : http://localhost:9001" -ForegroundColor Cyan
    } else {
        Write-Err "Echec du demarrage de l'agent"
    }
} else {
    Write-Host "`n   Pour demarrer l'agent Gabriel :" -ForegroundColor Yellow
    Write-Host "     .\start-agent.ps1" -ForegroundColor Cyan
    Write-Host "   ou uniquement le service agent :" -ForegroundColor Yellow
    Write-Host "     docker compose -f `"$ComposeFile`" -p $ProjectName up -d $ServiceMain" -ForegroundColor Cyan
}
