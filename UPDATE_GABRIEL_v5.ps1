#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Mise à jour Gabriel v5.0 avec socket cleanup

.DESCRIPTION
    Script pour mettre à jour Gabriel avec la nouvelle version
    qui ferme complètement le port quand l'agent s'arrête
#>

$ProjectRoot = "C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local"

Write-Host "=========================================="  -ForegroundColor Cyan
Write-Host "Gabriel v5.0 Update Script" -ForegroundColor Cyan
Write-Host "=========================================="  -ForegroundColor Cyan
Write-Host ""

# Arrêter tous les conteneurs
Write-Host "[STEP 1] Arrêt de Gabriel..." -ForegroundColor Yellow
Push-Location $ProjectRoot
docker compose down -v
Pop-Location

Write-Host "[OK] Tous les conteneurs sont arrêtés"  -ForegroundColor Green
Start-Sleep -Seconds 5

# Rebuild l'image avec les nouveaux fichiers
Write-Host "" 
Write-Host "[STEP 2] Rebuild de l'image Docker..." -ForegroundColor Yellow
Push-Location $ProjectRoot

docker compose build --no-cache

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Image rebuild avec succès" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Erreur rebuild" -ForegroundColor Red
    Pop-Location
    exit 1
}

# Relancer Gabriel
Write-Host ""
Write-Host "[STEP 3] Démarrage de Gabriel v5.0..." -ForegroundColor Yellow
docker compose up -d

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Gabriel v5.0 démarré" -ForegroundColor Green
    Write-Host ""
    Write-Host "=========================================="  -ForegroundColor Green
    Write-Host "Gabriel v5.0 est maintenant en cours d'exécution!"  -ForegroundColor Green
    Write-Host "Port: 8080"  -ForegroundColor Green
    Write-Host "Accès: http://localhost:8080"  -ForegroundColor Green
    Write-Host "=========================================="  -ForegroundColor Green
    Write-Host ""
    Write-Host "IMPORTANT:"  -ForegroundColor Yellow
    Write-Host "- Le port se fermera COMPLÈTEMENT quand vous taperez 'quitter'" -ForegroundColor Yellow
    Write-Host "- Docker Desktop ne sera PAS affecté" -ForegroundColor Yellow
    Write-Host "- Vous pouvez redémarrer immédiatement après"  -ForegroundColor Yellow
} else {
    Write-Host "[ERROR] Erreur démarrage" -ForegroundColor Red
    Pop-Location
    exit 1
}

Pop-Location
