#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Port Locker - Empêche d'autres processus de réoccuper le port Gabriel
    
.DESCRIPTION
    Crée un "blocker" qui occupe le port jusqu'à ce que Gabriel soit prêt
    Puis libère le port pour Gabriel
    
    Cela empêche Docker Desktop ou autres services de reprendre le port
#>

$Port = 8080
$PortLockFile = "$PSScriptRoot\.port-lock-8080"

function Lock-Port {
    param($Port)
    
    Write-Host "[Port Locker] 🔒 Verrouillage du port $Port..." -ForegroundColor Yellow
    
    # Créer un processus fantôme qui occupe le port
    $scriptBlock = {
        param($port)
        try {
            $listener = New-Object System.Net.Sockets.TcpListener([System.Net.IPAddress]::Any, $port)
            $listener.Start()
            Write-Host "[Port Locker] Port $port verrouillé" -ForegroundColor Green
            
            # Rester ouvert indéfiniment
            while ($true) { Start-Sleep -Seconds 60 }
        }
        catch {
            Write-Host "[Port Locker] ❌ Erreur: $_" -ForegroundColor Red
        }
    }
    
    # Lancer en background
    $job = Start-Job -ScriptBlock $scriptBlock -ArgumentList $Port
    
    # Sauvegarder le JobId
    $job.Id | Out-File -FilePath $PortLockFile -Encoding UTF8
    
    Write-Host "[Port Locker] ✅ Port $Port verrouillé (Job ID: $($job.Id))" -ForegroundColor Green
    return $job.Id
}

function Unlock-Port {
    param($Port)
    
    if (Test-Path $PortLockFile) {
        $jobId = Get-Content $PortLockFile
        Write-Host "[Port Locker] 🔓 Déverrouillage du port $Port (Job ID: $jobId)..." -ForegroundColor Yellow
        
        try {
            Stop-Job -Id $jobId -ErrorAction SilentlyContinue
            Remove-Job -Id $jobId -ErrorAction SilentlyContinue
            Remove-Item $PortLockFile -ErrorAction SilentlyContinue
            Write-Host "[Port Locker] ✅ Port $Port déverrouillé" -ForegroundColor Green
        }
        catch {
            Write-Host "[Port Locker] ⚠ Erreur: $_" -ForegroundColor Yellow
        }
    }
}

# Commandes
if ($args[0] -eq "lock") {
    Lock-Port -Port $Port
}
elseif ($args[0] -eq "unlock") {
    Unlock-Port -Port $Port
}
else {
    Write-Host "Usage: .\port-locker.ps1 [lock|unlock]" -ForegroundColor Cyan
}
