# =============================================================================
#  VARIATEUR_UN_CLIC.ps1
#  Transmission mécanique de correction autonome — UN CLIC
#
#  Ce script enchaîne automatiquement les 4 étages du variateur de
#  programmation de l'agent Gabriel MULTILOOP, en une seule commande :
#
#    1. ANALYSEUR   : scanne le dépôt → gabriel_repo_map.db (réseau neuronal)
#    2. ARCHIVISTE  : (transmission) retrouve les adresses via les mots-clés
#                     du PATCH dans le réseau (base SQLite)
#    3. ORCHESTRATEUR : applique la correction à TOUS les fichiers impliqués
#                     (avec copie de sauvegarde + manifeste restaurable)
#    4. TRANSMISSION UN CLIC : le point d'entrée unique (ci-dessous)
#
#  Usage (PowerShell) :
#     .\VARIATEUR_UN_CLIC.ps1 -Patch exemple_patch_correction.py
#     .\VARIATEUR_UN_CLIC.ps1 -Patch exemple_patch_correction.py -DryRun
#     .\VARIATEUR_UN_CLIC.ps1 -Rollback (dossier snapshot)
# =============================================================================

param(
    [string]$Patch = "",
    [switch]$DryRun,
    [string]$Rollback = ""
)

$ErrorActionPreference = "Stop"
$repo = "C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local"

Write-Host "`n═══════════════════════════════════════════════════"
Write-Host "  VARIATEUR MECANIQUE DE CORRECTION AUTONOME"
Write-Host "═══════════════════════════════════════════════════`n"

try {
    Push-Location $repo

    # ── Étape 0 : reconstruction de la base du réseau (analyseur) ──────────
    Write-Host "[1/4] ANALYSEUR - reconstruction de gabriel_repo_map.db (reseau neuronal)..."
    python orchestrator_main.py --rebuild
    if ($LASTEXITCODE -ne 0) { throw "echec analyseur" }

    # ── Étape 1 : rollback éventuel ─────────────────────────────────────────
    if ($Rollback -ne "") {
        Write-Host "`n[ROLLBACK] restauration du snapshot : $Rollback"
        python orchestrator_main.py --list-snapshots
        python orchestrator_main.py --rollback $Rollback
        return
    }

    # ── Étape 2 : vérifier qu'un patch a été fourni ─────────────────────────
    if ($Patch -eq "") {
        Write-Host "[2/4] Aucun patch fourni. Snapshots disponibles :"
        python orchestrator_main.py --list-snapshots
        throw "Fournir -Patch <fichier>.py  (exemple : exemple_patch_correction.py)"
    }
    if (-not (Test-Path $Patch)) { throw "Patch introuvable : $Patch" }

    # ── Étape 3 : transmission un clic (archiviste + orchestrateur) ────────
    Write-Host "[3/4] TRANSMISSION - archiviste + orchestrateur..."
    if ($DryRun) {
        python transmission_un_clic.py --patch $Patch --dry-run
    } else {
        python transmission_un_clic.py --patch $Patch
    }
    if ($LASTEXITCODE -ne 0) { throw "echec transmission" }

    # ── Étape 4 : rapport final ─────────────────────────────────────────────
    Write-Host "`n[4/4] FIN - correction appliquee au reseau neuronal.`n"
    Write-Host "Pour annuler :  python orchestrator_main.py --list-snapshots"
    Write-Host "Pour restaurer : python orchestrator_main.py --rollback <dossier>"
}
catch {
    Write-Host "`nERREUR : $_" -ForegroundColor Red
    exit 1
}
finally {
    Pop-Location
}