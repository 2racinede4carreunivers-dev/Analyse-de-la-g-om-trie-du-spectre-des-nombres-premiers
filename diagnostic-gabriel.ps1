#!/usr/bin/env powershell
# =============================================================================
#  diagnostic-gabriel.ps1 — Diagnostic complet, concu pour tourner dans une
#  VRAIE fenetre PowerShell Windows (detachee de VS Code).
#
#  Il ecrit TOUT dans un fichier log horodate que Cline relit ensuite, ET
#  affiche le detail a l'ecran dans la grande fenetre Windows.
#
#  Usage :
#    .\diagnostic-gabriel.ps1
#    .\diagnostic-gabriel.ps1 -StartAgent   # + demarre Gabriel a la fin
# =============================================================================
param(
    [switch]$StartAgent
)

$ProjectRoot = "C:\Analyse-de-la-geometrie-du-spectre-des-nombres-premiers\Analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers"
$ComposeFile = Join-Path $ProjectRoot "docker-compose.yml"
$ProjectName = "analyse-de-la-g-om-trie-du-spectre-des-nombres-premiers"
$LogFile = Join-Path $env:TEMP ("gabriel_diag_{0:yyyyMMdd_HHmmss}.log" -f (Get-Date))

function Section { param($t) Write-Host "`n==== $t ====" -ForegroundColor Cyan;  "==== $t ====" | Out-File $LogFile -Append -Encoding utf8 }
function Line    { param($t) Write-Host $t; $t | Out-File $LogFile -Append -Encoding utf8 }

"Diagnostic Gabriel  $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" | Out-File $LogFile -Encoding utf8
"PowerShell PID=$PID  Executable=$((Get-Process -Id $PID).Path)" | Out-File $LogFile -Append -Encoding utf8

Section "DOCKER"
docker info --format 'Docker OK : {{.ServerVersion}}' 2>&1 | ForEach-Object { Line $_ }

Section "CONTENEURS"
docker ps -a --format '{{.Names}} | {{.Image}} | {{.Status}} | {{.Ports}}' 2>&1 | ForEach-Object { Line $_ }

Section "OLLAMA - API"
try {
    $ver = (Invoke-WebRequest -Uri 'http://localhost:11434/api/version' -UseBasicParsing -TimeoutSec 5).Content
    Line "API /version : $ver"
    $tags = (Invoke-WebRequest -Uri 'http://localhost:11434/api/tags' -UseBasicParsing -TimeoutSec 5).Content | ConvertFrom-Json
    Line "Modeles presents :"
    $tags.models | ForEach-Object { Line ("  - {0}  ({1:N2} Go)" -f $_.name, ($_.size/1GB)) }
} catch {
    Line "ERREUR API Ollama : $($_.Exception.Message)"
}

Section "PORTS"
netstat -ano 2>&1 | Select-String ':11434|:9001|:8080' | ForEach-Object { Line $_.ToString() }

if ($StartAgent) {
    Section "DEMARRAGE AGENT"
    docker compose -f $ComposeFile -p $ProjectName up -d llm-agent-multiloop 2>&1 | ForEach-Object { Line $_ }
    Start-Sleep -Seconds 6
    docker ps --filter "name=llm-agent-multiloop-run" --format '{{.Names}} | {{.Status}} | {{.Ports}}' 2>&1 | ForEach-Object { Line $_ }
    Line "CLI interactif : docker attach llm-agent-multiloop-run"
    Line "HTTP API       : http://localhost:9001"
}

Section "FIN"
Line "Log complet : $LogFile"
Write-Host "`n>>> Log ecrit dans : $LogFile" -ForegroundColor Green
Write-Host ">>> Cline relit ce fichier automatiquement." -ForegroundColor Green
