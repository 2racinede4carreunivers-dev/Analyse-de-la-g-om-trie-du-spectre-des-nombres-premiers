#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Gabriel Launcher - Gestion propre de Gabriel avec PowerShell ISE
    
.DESCRIPTION
    Démarre/arrête Gabriel sans fermer Docker Desktop
    Gère les ports de manière fiable
    
.EXAMPLE
    .\gabriel.ps1 start
    .\gabriel.ps1 stop
    .\gabriel.ps1 restart
    .\gabriel.ps1 status
#>

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("start", "stop", "restart", "status", "logs")]
    [string]$Command = "status"
)

# Configuration
$ProjectRoot = "C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local"
$Port = 8080
$ContainerName = "llm-agent-multiloop-run"

function Write-Status {
    param($Message, $Type = "Info")
    $colors = @{
        "Success" = "Green"
        "Error"   = "Red"
        "Warning" = "Yellow"
        "Info"    = "Cyan"
    }
    Write-Host "[$Type] $Message" -ForegroundColor $colors[$Type]
}

function Check-Port {
    param($Port)
    try {
        $netstat = netstat -ano | Select-String ":$Port"
        if ($netstat) {
            $parts = $netstat -split '\s+' | Where-Object {$_}
            $pid = $parts[-1]
            return @{
                Occupied = $true
                PID = $pid
                Process = (Get-Process -Id $pid -ErrorAction SilentlyContinue).ProcessName
            }
        }
        return @{Occupied = $false}
    }
    catch {
        return @{Occupied = $false}
    }
}

function Start-Gabriel {
    Write-Status "Demarrage de Gabriel..." "Info"
    
    $portStatus = Check-Port -Port $Port
    if ($portStatus.Occupied) {
        Write-Status "ATTENTION: Port $Port occupe par PID $($portStatus.PID) ($($portStatus.Process))" "Warning"
        Write-Status "NE JAMAIS tuer ce processus (fermerait Docker Desktop)" "Error"
        Write-Status "SOLUTION: Executez d abord: .\gabriel.ps1 stop" "Info"
        return $false
    }
    
    try {
        Push-Location $ProjectRoot
        Write-Status "Repertoire: $ProjectRoot" "Info"
        
        Write-Status "Lancement des conteneurs Docker..." "Info"
        docker compose up -d
        
        if ($LASTEXITCODE -eq 0) {
            Write-Status "Conteneurs lances" "Success"
            Write-Status "Attente du demarrage complet (20 secondes)..." "Info"
            Start-Sleep -Seconds 20
            
            Write-Status "GABRIEL ACCESSIBLE: http://localhost:$Port" "Success"
            Write-Status "Commande d arret: .\gabriel.ps1 stop" "Info"
            return $true
        }
        else {
            Write-Status "Erreur au demarrage" "Error"
            return $false
        }
    }
    finally {
        Pop-Location
    }
}

function Stop-Gabriel {
    Write-Status "Arret de Gabriel..." "Info"
    
    try {
        Push-Location $ProjectRoot
        
        Write-Status "Arret des conteneurs Docker..." "Info"
        docker compose down
        
        if ($LASTEXITCODE -eq 0) {
            Write-Status "Conteneurs arretes proprement" "Success"
            Start-Sleep -Seconds 3
            
            $portStatus = Check-Port -Port $Port
            if ($portStatus.Occupied) {
                Write-Status "ATTENTION: Port $Port toujours occupe par PID $($portStatus.PID)" "Warning"
                Write-Status "Attendez quelques secondes que Docker se stabilise" "Info"
            }
            else {
                Write-Status "Port $Port libere" "Success"
            }
            return $true
        }
        else {
            Write-Status "Erreur a l arret" "Error"
            return $false
        }
    }
    finally {
        Pop-Location
    }
}

function Restart-Gabriel {
    Write-Status "Redemarrage complet..." "Info"
    Stop-Gabriel
    Start-Sleep -Seconds 2
    Start-Gabriel
}

function Show-Status {
    Write-Host ""
    Write-Host "====== Gabriel Multi-Loop Status ======" -ForegroundColor Cyan
    Write-Host ""
    
    # Etat de Docker
    try {
        $dockerInfo = docker ps 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Status "Docker Desktop: ACTIF" "Success"
        }
        else {
            Write-Status "Docker Desktop: NON REPONDANT" "Error"
            Write-Status "Action: Redemarrez Docker Desktop" "Warning"
        }
    }
    catch {
        Write-Status "Docker Desktop: ERREUR" "Error"
    }
    
    Write-Host ""
    
    # Etat du conteneur Gabriel
    try {
        $container = docker ps | Select-String $ContainerName
        if ($container) {
            Write-Status "Gabriel Container: ACTIF" "Success"
            Write-Status "Acces: http://localhost:$Port" "Info"
        }
        else {
            Write-Status "Gabriel Container: ARRÊTE" "Warning"
            Write-Status "Commande: .\gabriel.ps1 start" "Info"
        }
    }
    catch {
        Write-Status "Gabriel Container: ERREUR" "Error"
    }
    
    Write-Host ""
    
    # Etat du port
    $portStatus = Check-Port -Port $Port
    if ($portStatus.Occupied) {
        Write-Status "Port $Port : OCCUPE (PID $($portStatus.PID))" "Warning"
    }
    else {
        Write-Status "Port $Port : LIBRE" "Success"
    }
    
    Write-Host ""
    Write-Host "====== Commandes ======" -ForegroundColor Cyan
    Write-Host ".\gabriel.ps1 start    - Demarrer Gabriel" -ForegroundColor Cyan
    Write-Host ".\gabriel.ps1 stop     - Arreter Gabriel" -ForegroundColor Cyan
    Write-Host ".\gabriel.ps1 restart  - Redemarrer Gabriel" -ForegroundColor Cyan
    Write-Host ".\gabriel.ps1 logs     - Voir les logs" -ForegroundColor Cyan
    Write-Host ""
}

function Show-Logs {
    Write-Status "Logs Gabriel (derniere 30 lignes)..." "Info"
    Write-Host ""
    docker logs --tail 30 $ContainerName
    Write-Host ""
}

# Execution
switch ($Command) {
    "start"   { Start-Gabriel }
    "stop"    { Stop-Gabriel }
    "restart" { Restart-Gabriel }
    "logs"    { Show-Logs }
    "status"  { Show-Status }
    default   { Show-Status }
}
