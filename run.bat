@echo off
echo ========================================
echo    DrawSign v2.0 - Starting
echo ========================================

if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found
    echo Run setup.py first
    pause
    exit /b 1
)

venv\Scripts\python.exe drawbot_edusign.py
pause
