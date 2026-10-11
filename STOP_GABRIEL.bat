@echo off
REM ============================================================
REM Gabriel Shutdown Script
REM Double-click pour arrêter Gabriel proprement
REM ============================================================

SETLOCAL ENABLEDELAYEDEXPANSION

cd /D "%~dp0"

echo.
echo ============================================================
echo     Arrêt de Gabriel (Port 8080)
echo ============================================================
echo.
echo IMPORTANT: Cela arrête tous les conteneurs proprement
echo IMPORTANTE: Ne fermez PAS cette fenêtre avant la fin!
echo.

REM Lancer PowerShell avec le script gabriel.ps1
powershell -NoExit -ExecutionPolicy Bypass -File gabriel.ps1 stop

pause
