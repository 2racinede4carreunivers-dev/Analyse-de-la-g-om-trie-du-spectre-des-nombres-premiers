@echo off
REM ============================================================================
REM run-tests.bat
REM Lance la suite pytest de Gabriel - double-clic friendly
REM Usage : double-clic OU 'run-tests.bat' dans cmd.exe
REM ============================================================================

REM Aller au dossier du script
cd /d "%~dp0"

REM Forcer UTF-8 dans la console
chcp 65001 >nul

cls
echo ================================================================================
echo     GABRIEL MULTI-LOOP - SUITE DE TESTS PYTEST
echo ================================================================================
echo.
echo   Dossier : %CD%
echo.

REM Verifier Python
where python >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH.
    echo Installez Python 3.11+ depuis https://python.org
    pause
    exit /b 1
)

echo [1/2] Verification de pytest...
python -c "import pytest" 2>nul
if errorlevel 1 (
    echo   pytest manquant, installation...
    python -m pip install pytest pytest-asyncio --quiet
    if errorlevel 1 (
        echo [ERREUR] Echec installation pytest.
        pause
        exit /b 1
    )
)
echo   OK pytest disponible.
echo.

echo [2/2] Execution des tests Gabriel...
echo.

python -m pytest tests/ -v --tb=short --color=yes
set EXITCODE=%ERRORLEVEL%

echo.
echo ================================================================================
if %EXITCODE%==0 (
    echo     RESULTAT : TOUS LES TESTS PASSENT
) else (
    echo     RESULTAT : DES TESTS ONT ECHOUE - voir details ci-dessus
)
echo ================================================================================
echo.

echo Astuces :
echo   Un seul fichier : python -m pytest tests\test_audit_store.py -v
echo   Un seul test    : python -m pytest tests\test_audit_store.py::test_save_record -v
echo   Coverage        : python -m pytest --cov=src
echo.

pause
exit /b %EXITCODE%
