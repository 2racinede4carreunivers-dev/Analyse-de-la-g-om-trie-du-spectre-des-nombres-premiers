# =============================================================================
#  clean-docker.ps1  |  Nettoyage Docker complet
#
#  Usage:
#    .\clean-docker.ps1           # nettoyage standard
#    .\clean-docker.ps1 -Hard     # nettoyage AGRESSIF (supprime tout)
#    .\clean-docker.ps1 -ShrinkWSL # tente de compacter le disque WSL2
#
#  ATTENTION: -Hard supprime TOUTES vos images Docker (pas seulement celles
#  de ce projet). N'utilisez que si vous etes sur d'avoir trop d'images.
# =============================================================================

param(
    [switch]$Hard,
    [switch]$ShrinkWSL
)

$C_OK = "Green"; $C_WARN = "Yellow"; $C_ERR = "Red"; $C_INFO = "Cyan"

function Write-Step { param([string]$M) Write-Host "`n>  $M" -ForegroundColor $C_INFO }
function Write-OK   { param([string]$M) Write-Host "   OK  $M" -ForegroundColor $C_OK }
function Write-Warn { param([string]$M) Write-Host "   !!  $M" -ForegroundColor $C_WARN }

Clear-Host
Write-Host @"

  +============================================================+
  |   DOCKER CLEANUP  -  Multi-Loop Agent Gabriel              |
  |   Recupere l'espace disque utilise par Docker / WSL2       |
  +============================================================+

"@ -ForegroundColor Magenta

# Etat avant
Write-Step "Etat actuel Docker"
docker system df 2>&1
Write-Host ""

# 1. Arret de tous les conteneurs en cours
Write-Step "Arret de tous les conteneurs en cours"
$running = docker ps -q 2>$null
if ($running) {
    docker stop $running 2>$null | Out-Null
    Write-OK "Conteneurs arretes."
} else {
    Write-OK "Aucun conteneur actif."
}

# 2. Suppression des conteneurs stoppes
Write-Step "Suppression des conteneurs stoppes"
docker container prune -f 2>&1 | Out-Null
Write-OK "Conteneurs stoppes supprimes."

# 3. Suppression des builds incomplets (build cache)
Write-Step "Suppression du cache de build Docker"
docker builder prune -a -f 2>&1 | Out-String | Write-Host -ForegroundColor DarkGray
Write-OK "Cache build vide."

if ($Hard) {
    # 4. Suppression de TOUTES les images (mode agressif)
    Write-Warn "MODE HARD : suppression de TOUTES les images Docker"
    $confirm = Read-Host "Confirmer ? (tapez OUI en majuscules)"
    if ($confirm -eq "OUI") {
        docker image prune -a -f 2>&1 | Out-String | Write-Host -ForegroundColor DarkGray
        Write-OK "Toutes les images supprimees."
    } else {
        Write-Warn "Annule."
    }

    # Volumes orphelins
    Write-Step "Suppression des volumes orphelins"
    docker volume prune -f 2>&1 | Out-String | Write-Host -ForegroundColor DarkGray
    Write-OK "Volumes orphelins supprimes."

    # Reseaux orphelins
    Write-Step "Suppression des reseaux orphelins"
    docker network prune -f 2>&1 | Out-String | Write-Host -ForegroundColor DarkGray
    Write-OK "Reseaux orphelins supprimes."
} else {
    # Mode standard : seulement les images "dangling" (sans tag)
    Write-Step "Suppression des images sans tag (dangling)"
    docker image prune -f 2>&1 | Out-String | Write-Host -ForegroundColor DarkGray
    Write-OK "Images dangling supprimees."
}

# Etat apres
Write-Step "Etat Docker apres nettoyage"
docker system df 2>&1
Write-Host ""

# WSL2 shrink (le disque virtuel ne se reduit pas seul)
if ($ShrinkWSL) {
    Write-Step "Compactage du disque WSL2 (peut prendre quelques minutes)"
    Write-Warn "Docker Desktop va etre arrete pour ca."

    # Arret Docker Desktop
    Get-Process "Docker Desktop" -ErrorAction SilentlyContinue | Stop-Process -Force
    Start-Sleep -Seconds 5

    # Arret WSL
    wsl --shutdown
    Start-Sleep -Seconds 3

    # Localiser le vhdx
    $vhdxPaths = @(
        "$env:LOCALAPPDATA\Docker\wsl\data\ext4.vhdx",
        "$env:LOCALAPPDATA\Docker\wsl\disk\docker_data.vhdx",
        "$env:LOCALAPPDATA\Packages\CanonicalGroupLimited.UbuntuonWindows*\LocalState\ext4.vhdx"
    )
    foreach ($pattern in $vhdxPaths) {
        $found = Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue
        foreach ($vhdx in $found) {
            Write-Host "   Compactage : $($vhdx.FullName)" -ForegroundColor DarkGray
            $beforeSize = (Get-Item $vhdx.FullName).Length / 1GB
            $diskpartScript = @"
select vdisk file="$($vhdx.FullName)"
attach vdisk readonly
compact vdisk
detach vdisk
exit
"@
            $tmp = New-TemporaryFile
            $diskpartScript | Out-File -FilePath $tmp.FullName -Encoding ASCII
            diskpart /s $tmp.FullName | Out-Null
            Remove-Item $tmp.FullName -Force
            $afterSize = (Get-Item $vhdx.FullName).Length / 1GB
            Write-OK ("Compactage termine : {0:N1} Go -> {1:N1} Go" -f $beforeSize, $afterSize)
        }
    }
    Write-OK "WSL2 compacte. Relancez Docker Desktop manuellement."
}

Write-Host ""
Write-Host "==================================================" -ForegroundColor Magenta
Write-Host "  NETTOYAGE TERMINE"                                -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Magenta
Write-Host ""
Write-Host "  Pour reconstruire l'agent proprement :" -ForegroundColor Cyan
Write-Host "     .\start-agent.ps1 -Rebuild"           -ForegroundColor White
Write-Host ""
