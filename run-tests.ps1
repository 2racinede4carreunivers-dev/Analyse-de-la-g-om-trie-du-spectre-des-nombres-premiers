# ============================================================================
# run-tests.ps1
# Script PowerShell pour lancer la suite complete pytest de Gabriel
# Usage : double-clic OU '.\run-tests.ps1' dans PowerShell
# ============================================================================

# Forcer encodage UTF-8 (pour les accents et caracteres mathematiques)
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Couleurs
function Write-Color($Text, $Color = "White") {
    Write-Host $Text -ForegroundColor $Color
}

# Aller au dossier du script
Set-Location -Path $PSScriptRoot

Clear-Host
Write-Color "================================================================================" "Cyan"
Write-Color "    GABRIEL MULTI-LOOP - SUITE DE TESTS PYTEST" "Cyan"
Write-Color "================================================================================" "Cyan"
Write-Color ""
Write-Color "  Dossier      : $PSScriptRoot" "Gray"
Write-Color "  Mode         : execution locale (sans Docker)" "Gray"
Write-Color ""

# Verifier que Python est dispo
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Color "[ERREUR] Python n'est pas installe ou pas dans le PATH." "Red"
    Write-Color "Installez Python 3.11+ depuis https://python.org" "Yellow"
    Read-Host "Appuyez sur Entree pour fermer"
    exit 1
}

Write-Color "[1/3] Verification des dependances pytest..." "Yellow"
$pytestCheck = python -c "import pytest" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Color "  pytest n'est pas installe. Installation en cours..." "Yellow"
    python -m pip install pytest pytest-asyncio --quiet
    if ($LASTEXITCODE -ne 0) {
        Write-Color "[ERREUR] Impossible d'installer pytest." "Red"
        Read-Host "Appuyez sur Entree pour fermer"
        exit 1
    }
}
Write-Color "  OK : pytest disponible." "Green"
Write-Color ""

Write-Color "[2/3] Execution de la suite complete (tests/)..." "Yellow"
Write-Color "  Cela peut prendre quelques secondes..." "Gray"
Write-Color ""

# Lancer pytest avec verbose + couleur + resume
python -m pytest tests/ -v --tb=short --color=yes
$exitCode = $LASTEXITCODE

Write-Color ""
Write-Color "================================================================================" "Cyan"
if ($exitCode -eq 0) {
    Write-Color "    RESULTAT : TOUS LES TESTS PASSENT - GABRIEL EST PRET" "Green"
} else {
    Write-Color "    RESULTAT : DES TESTS ONT ECHOUE (voir details ci-dessus)" "Red"
}
Write-Color "================================================================================" "Cyan"
Write-Color ""

# Optionnel : sauvegarder le rapport dans data/
$reportDir = Join-Path $PSScriptRoot "data\test-reports"
if (-not (Test-Path $reportDir)) {
    New-Item -ItemType Directory -Path $reportDir -Force | Out-Null
}
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$reportFile = Join-Path $reportDir "report-$timestamp.txt"
python -m pytest tests/ --tb=short --no-header 2>&1 | Out-File -FilePath $reportFile -Encoding UTF8
Write-Color "  Rapport sauvegarde : $reportFile" "Gray"
Write-Color ""

Write-Color "[3/3] Astuces :" "Yellow"
Write-Color "  - Pour lancer un seul fichier : python -m pytest tests\test_audit_store.py -v" "Gray"
Write-Color "  - Pour un seul test           : python -m pytest tests\test_audit_store.py::test_save_record -v" "Gray"
Write-Color "  - Pour les marqueurs          : python -m pytest -m 'not slow'" "Gray"
Write-Color "  - Pour le coverage            : python -m pytest --cov=src" "Gray"
Write-Color ""
Write-Color "Appuyez sur Entree pour fermer..." "DarkGray"
Read-Host

exit $exitCode
