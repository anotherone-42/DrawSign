@echo off
echo ========================================
echo    DrawBot Edusign - Demarrage
echo ========================================

if not exist "venv\" (
    echo [ERREUR] Venv inexistant
    echo Lancez setup.bat d'abord
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
python drawbot_edusign.py
pause