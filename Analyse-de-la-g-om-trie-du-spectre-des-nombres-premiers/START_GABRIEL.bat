@echo off
REM ============================================================
REM Gabriel Launcher Batch File
REM Double-click pour démarrer Gabriel directement
REM ============================================================

SETLOCAL ENABLEDELAYEDEXPANSION

cd /D "%~dp0"

echo.
echo ============================================================
echo     Gabriel Multi-Loop Mathematical Agent v5.4
echo ============================================================
echo.
echo Demarrage de Gabriel sur port 8080...
echo.

REM Lancer PowerShell avec le script gabriel.ps1
powershell -NoExit -ExecutionPolicy Bypass -File gabriel.ps1 start

REM Le -NoExit garde PowerShell ouvert après exécution
REM Cela permet de voir les résultats et d'exécuter d'autres commandes

pause
