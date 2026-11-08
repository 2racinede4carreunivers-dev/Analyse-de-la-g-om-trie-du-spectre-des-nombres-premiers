@echo off
REM ========================================================================
REM  Quick Start - Agent Gabriel
REM  Lance automatiquement le script start-agent.ps1 avec les bons chemin
REM ========================================================================

REM Chemin du projet
set "PROJECT_DIR=C:\agent-multiloop-Gabriel-local-final\agent-multiloop-Gabriel-local"

REM Vérifier que le dossier existe
if not exist "%PROJECT_DIR%" (
    echo ERREUR: Dossier non trouvé: %PROJECT_DIR%
    echo Vérifiez que le chemin est correct.
    pause
    exit /b 1
)

REM Naviguer vers le dossier
cd /d "%PROJECT_DIR%"

REM Afficher le chemin
echo.
echo ========================================================
echo  AGENT GABRIEL - Quick Start
echo ========================================================
echo Chemin: %PROJECT_DIR%
echo.

REM Lancer le script PowerShell
powershell -NoExit -ExecutionPolicy Bypass -Command "& '.\start-agent.ps1'"

pause
