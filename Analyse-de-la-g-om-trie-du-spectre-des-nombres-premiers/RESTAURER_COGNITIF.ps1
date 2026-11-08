# =============================================================================
#  RESTAURER_COGNITIF.ps1
#  Protection des capacites cognitives — snapshot / rollback en UNE COMMANDE
#
#  Ce script protege le coeur cognitif/expert de l'agent
#  "La fiancee de Cline Mm. Gabriel multiloop local" (pipeline cognitif
#  convolutif, moteurs, systeme spectral, pipeline HOL, corpus).
#
#  Usage (PowerShell) :
#     .\RESTAURER_COGNITIF.ps1 -Snapshot                  # snapshot de reference
#     .\RESTAURER_COGNITIF.ps1 -Snapshot mon_label        # snapshot nomme
#     .\RESTAURER_COGNITIF.ps1 -List                      # lister les snapshots
#     .\RESTAURER_COGNITIF.ps1 -Rollback <nom_snapshot>   # RESTAURER (une commande)
#     .\RESTAURER_COGNITIF.ps1 -Verifier <nom_snapshot>   # verifier l'integrite
#     .\RESTAURER_COGNITIF.ps1 -Rollback <nom> -DryRun    # simulation
# =============================================================================

param(
    [string]$Snapshot = "",
    [switch]$List,
    [string]$Rollback = "",
    [string]$Verifier = "",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$repo = $PSScriptRoot

Write-Host "`n═══════════════════════════════════════════════════"
Write-Host "  PROTECTION DU COEUR COGNITIF — La fiancee de Cline"
Write-Host "═══════════════════════════════════════════════════`n"

try {
    Push-Location $repo

    if ($List) {
        python src/multiloop/protection_cognitive.py --list
        return
    }

    if ($Verifier -ne "") {
        python src/multiloop/protection_cognitive.py --verifier $Verifier
        return
    }

    if ($Rollback -ne "") {
        if ($DryRun) {
            python src/multiloop/protection_cognitive.py --rollback $Rollback --dry-run
        } else {
            Write-Host "[ROLLBACK] restauration de l'ancienne version du coeur cognitif..."
            python src/multiloop/protection_cognitive.py --rollback $Rollback
        }
        return
    }

    # Snapshot (par defaut si aucune option)
    if ($Snapshot -eq "") { $Snapshot = "reference" }
    python src/multiloop/protection_cognitive.py --snapshot $Snapshot
}
catch {
    Write-Host "`nERREUR : $_" -ForegroundColor Red
    exit 1
}
finally {
    Pop-Location
}